import time

class MetricsEngine:
    """Scientific engine for calculating ergonomic and typing performance metrics."""
    
    def __init__(self):
        self.data = {
            'wpm': 0, 'accuracy': 0, 'completion_time': 0,
            'error_rate': 0, 'finger_movement_distance': 0,
            'home_row_retention': 0, 'correction_time': 0,
            'total_typing_time': 0, 'navigational_key_usage': 0,
            'backspace_usage': 0, 'pageup_pagedown_usage': 0,
            'delete_usage': 0, 'cognitive_load': 0
        }
        self.start_time = None
        self.char_count = 0
        self.error_count = 0

    def start_session(self):
        self.start_time = time.time()

    def update_metrics(self, typed_char, target_char, key_distances):
        """Processes a single keystroke and updates the scientific model."""
        if typed_char == target_char:
            self.char_count += 1
        else:
            self.error_count += 1
            
        # Sophisticated distance calculation logic would go here
        # (Simplified for the refactor skeleton)
        if typed_char in key_distances:
            self.data['finger_movement_distance'] += key_distances[typed_char]

    def finalize(self):
        """Calculates the final session metrics."""
        duration = time.time() - self.start_time
        self.data['total_typing_time'] = duration
        self.data['wpm'] = (self.char_count / 5) / (duration / 60) if duration > 0 else 0
        self.data['accuracy'] = (self.char_count / (self.char_count + self.error_count)) * 100 if (self.char_count + self.error_count) > 0 else 0
        return self.data
