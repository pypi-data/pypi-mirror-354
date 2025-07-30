import cv2
import numpy as np
import mss
import time
from ultralytics import YOLO
from .json_handler import JSONHandler
from datetime import datetime
from typing import Optional, Tuple, Dict, Any, Callable, List # Add List

class ScreenDetector:
    def __init__(self, model_path: str,
                 target_class_names: Optional[List[str]] = None, # Changed to target_class_names
                 json_file: str = "screen_detections.json",
                 confidence_threshold: float = 0.5,
                 clean_output: bool = False,
                 monitor_index: int = 1):
        if not clean_output:
            print(f"Loading YOLO model: {model_path}")

        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.json_handler = JSONHandler(json_file)
        self.running = False
        self.clean_output = clean_output
        self.last_click_status = None
        self.detection_callback = None

        # New: Store class names and map them to IDs
        self.class_names_to_ids = {}
        if hasattr(self.model, 'names'):
            self.class_names_to_ids = {name: int(idx) for idx, name in self.model.names.items()}
            if not clean_output:
                print(f"Available classes in model: {self.model.names}")

        self.target_class_ids = []
        if target_class_names:
            for name in target_class_names:
                if name in self.class_names_to_ids:
                    self.target_class_ids.append(self.class_names_to_ids[name])
                else:
                    print(f"Warning: Class '{name}' not found in model's classes. It will not be detected.")
        else:
            # If no specific names are provided, detect all classes in the model
            self.target_class_ids = list(self.class_names_to_ids.values())


        with mss.mss() as sct:
            self.monitor = sct.monitors[monitor_index]

        if not clean_output:
            print(f"Model loaded successfully")
            print(f"Screen resolution: {self.monitor['width']}x{self.monitor['height']}")
            print(f"Target class IDs for detection: {self.target_class_ids}") # Changed output
            print(f"Confidence threshold: {confidence_threshold}")


    def capture_screen(self) -> np.ndarray:
        with mss.mss() as sct:
            screenshot = sct.grab(self.monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            return frame

    def detect_object(self, frame: np.ndarray) -> Tuple[List[Dict[str, Any]], bool]: # Updated return type
        """
        Detects objects in the given frame and returns a list of detected target objects.
        :param frame: The image frame to detect objects in.
        :return: A tuple containing:
                 - A list of dictionaries, where each dictionary represents a detected target object
                   and includes 'x', 'y', 'confidence', 'class_id', 'class_name'.
                 - A boolean indicating if any target object was found (True) or not (False).
        """
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)

        detected_objects = []
        object_found = False

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])

                    # Check if the detected class ID is in our target_class_ids
                    if class_id in self.target_class_ids:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)
                        class_name = self.model.names.get(class_id, f"Unknown_{class_id}")
                        detected_objects.append({
                            "x": center_x,
                            "y": center_y,
                            "confidence": confidence,
                            "class_id": class_id,
                            "class_name": class_name
                        })
                        object_found = True # At least one target object is found

        return detected_objects, object_found

    def single_detection(self) -> Tuple[List[Dict[str, Any]], bool]: # Updated return type
        """
        Performs a single screen capture and object detection, saving results to JSON.
        :return: A tuple containing:
                 - A list of dictionaries, each representing a detected target object.
                 - A boolean indicating if any target object was found.
        """
        frame = self.capture_screen()
        detections, click = self.detect_object(frame) # Get list of detections and overall click status
        self.json_handler.save_detection(detections, click, self.monitor) # Pass the list

        if not self.clean_output:
            if click:
                print(f"Objects FOUND: {len(detections)} object(s) detected.")
                for obj in detections:
                    print(f"  - Class: {obj['class_name']} ({obj['x']}, {obj['y']}) - confidence: {obj['confidence']:.3f}")
            else:
                print(f"Object NOT FOUND")

        # Call callback if set
        if self.detection_callback:
            self.detection_callback(detections, click) # Pass the list and overall click status

        return detections, click # Return the list of detections and overall click status

    def start_continuous_detection(self, update_interval: float = 0.5,
                                   duration: Optional[int] = None,
                                   callback: Optional[Callable] = None): # Signature might need update
        """
        Starts continuous object detection on the screen.
        :param update_interval: Time in seconds between screen captures and detections.
        :param duration: Total time in seconds to run the detection. If None, runs indefinitely.
        :param callback: Optional callback function to execute after each detection.
                         It should accept (List[Dict[str, Any]], bool) as arguments.
        """
        self.running = True
        self.detection_callback = callback
        start_time = time.time()

        if not self.clean_output:
            print(f"Starting continuous detection (confidence: {self.confidence_threshold})")
            target_class_names_str = ', '.join([self.model.names.get(tid, f'ID_{tid}') for tid in self.target_class_ids])
            print(f"Target classes: {target_class_names_str if target_class_names_str else 'All available classes'}")
            if duration:
                print(f"Runtime: {duration} seconds")
            else:
                print("Runtime: infinite (press Ctrl+C to stop)")

        while self.running:
            try:
                frame = self.capture_screen()
                detections, click = self.detect_object(frame) # Get list of detections and overall click status
                self.json_handler.save_detection(detections, click, self.monitor) # Pass the list

                timestamp = datetime.now().strftime("%H:%M:%S")

                if self.clean_output:
                    if self.last_click_status != click:
                        if click:
                            print(f"[{timestamp}] FOUND: {len(detections)} object(s)")
                            for obj in detections:
                                print(f"  - {obj['class_name']} ({obj['x']}, {obj['y']}) conf:{obj['confidence']:.3f}")
                        else:
                            print(f"[{timestamp}] LOST")
                        self.last_click_status = click
                else:
                    if click:
                        print(f"[{timestamp}] Objects found: {len(detections)} object(s)")
                        for obj in detections:
                            print(f"  - {obj['class_name']} ({obj['x']}, {obj['y']}) - confidence: {obj['confidence']:.3f}")
                    else:
                        print(f"[{timestamp}] Object not found")


                if self.detection_callback:
                    self.detection_callback(detections, click) # Pass the list and overall click status


                if duration and (time.time() - start_time) >= duration:
                    print(f"\nRuntime {duration} seconds completed. Stopping...")
                    break

                time.sleep(update_interval)

            except Exception as e:
                print(f"Detection error: {e}")
                time.sleep(1)

    def set_confidence_threshold(self, new_threshold: float):
        """
        Sets a new confidence threshold for object detection.
        :param new_threshold: The new confidence threshold (0.0-1.0).
        """
        if 0.0 <= new_threshold <= 1.0:
            old_threshold = self.confidence_threshold
            self.confidence_threshold = new_threshold
            if not self.clean_output:
                print(f"Confidence threshold: {old_threshold} → {new_threshold}")
        else:
            raise ValueError(f"Invalid confidence threshold: {new_threshold} (must be 0.0-1.0)")

    def set_detection_callback(self, callback: Callable[[List[Dict[str, Any]], bool], None]):
        """
        Sets a callback function to be called after each detection.
        The callback function should accept two arguments:
        - detections: A list of dictionaries, each representing a detected object.
        - click: True if any target object was detected, False otherwise.
        """
        self.detection_callback = callback

    def get_model_info(self) -> Dict[str, Any]:
        """
        Returns information about the loaded model and detector settings.
        """
        return {
            "classes_in_model": self.model.names if hasattr(self.model, 'names') else "Unknown",
            "target_class_ids_for_detection": self.target_class_ids, # Updated
            "confidence_threshold": self.confidence_threshold,
            "screen_resolution": f"{self.monitor['width']}x{self.monitor['height']}"
        }

    def get_current_detection(self) -> Optional[Dict[str, Any]]:
        """
        Loads and returns the most recent detection data from the JSON file.
        """
        return self.json_handler.load_detection()

    def get_detection_history(self) -> list:
        """
        Loads and returns the detection history.
        """
        return self.json_handler.get_detection_history()

    def print_status(self):
        """
        Prints the current detection status to the console.
        """
        self.json_handler.print_current_status()

    def stop_detection(self):
        """
        Stops the continuous detection loop.
        """
        self.running = False
        if not self.clean_output:
            print("Detection stopped")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_detection()