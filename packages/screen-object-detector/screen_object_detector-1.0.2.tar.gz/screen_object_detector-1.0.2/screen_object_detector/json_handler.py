import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List


class JSONHandler:
    def __init__(self, json_file: str = "screen_detections.json"):
        self.json_file = json_file
        self._ensure_json_file_exists()

    def _ensure_json_file_exists(self):
        json_dir = os.path.dirname(self.json_file) if os.path.dirname(self.json_file) else '.'
        os.makedirs(json_dir, exist_ok=True)

        if not os.path.exists(self.json_file):
            initial_data = {
                "timestamp": datetime.now().isoformat(),
                "detected_objects": [], # Changed to a list
                "click": False,
                "screen_resolution": None
            }
            try:
                with open(self.json_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=2, ensure_ascii=False)
                print(f"Created JSON file: {self.json_file}")
            except Exception as e:
                print(f"Error creating JSON file: {e}")

    def save_detection(self, detections: List[Dict[str, Any]], click: bool,
                       monitor_info: Dict[str, Any]):
        """
        Saves the current detection data to the JSON file.
        :param detections: A list of dictionaries, each representing a detected object.
        :param click: True if any target object was detected, False otherwise.
        :param monitor_info: Dictionary containing monitor width and height.
        """
        detection_data = {
            "timestamp": datetime.now().isoformat(),
            "detected_objects": detections, # New field
            "click": click,
            "screen_resolution": f"{monitor_info.get('width', 0)}x{monitor_info.get('height', 0)}"
        }

        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(detection_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving JSON: {e}")

    def load_detection(self) -> Optional[Dict[str, Any]]:
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None

    def get_detection_history(self, history_file: Optional[str] = None) -> List[Dict[str, Any]]:
        if history_file is None:
            base_name = self.json_file.replace('.json', '')
            history_file = f"{base_name}_history.json"

        current_data = self.load_detection()
        if current_data is None:
            return []

        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []

        history.append(current_data)

        # Keep only last 100 records
        if len(history) > 100:
            history = history[-100:]

        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")

        return history

    def print_current_status(self):
        data = self.load_detection()
        if data:
            print(f"\nCurrent detection status:")
            print(f"   Time: {data['timestamp']}")
            print(f"   Object detected: {data['click']}")
            if data['detected_objects']:
                print("   Detected Objects:")
                for obj in data['detected_objects']:
                    print(f"     - Class: {obj.get('class_name', 'N/A')} (ID: {obj.get('class_id', 'N/A')})")
                    print(f"       Coords: ({obj.get('x', 'None')}, {obj.get('y', 'None')})")
                    print(f"       Confidence: {obj.get('confidence', 0.0):.3f}")
            else:
                print("   No specific objects detected.")
            if 'screen_resolution' in data:
                print(f"   Resolution: {data['screen_resolution']}")
            print()
        else:
            print("No detection data found\n")

    def clear_detection_data(self):
        # This method still just ensures the file exists with initial data,
        # effectively clearing previous content.
        self._ensure_json_file_exists()