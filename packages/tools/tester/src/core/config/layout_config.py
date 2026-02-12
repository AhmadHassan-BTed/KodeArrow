class TesterConfig:
    """Standardized key distances and ergonomic constants for the QTT suite."""
    
    LAPTOP_DISTANCES = {
        'backspace': 10,
        'delete': 11.5,
        'page up': 16,
        'page down': 16.5,
        'home': 15.5,
        'end': 17,
        'i': 3, 'j': 1, 'k': 2, 'l': 3,
        'u': 2, 'o': 3, 'p': 4, ';': 4,
        '[': 5, "'": 5
    }

    DESKTOP_DISTANCES = {
        'backspace': 15,
        'delete': 20,
        'page up': 25,
        'page down': 25.5,
        'home': 22,
        'end': 23,
        'i': 3, 'j': 1, 'k': 2, 'l': 3,
        'u': 2, 'o': 3, 'p': 4, ';': 4,
        '[': 5, "'": 5
    }

    @staticmethod
    def get_distances(mode="laptop"):
        return TesterConfig.LAPTOP_DISTANCES if mode == "laptop" else TesterConfig.DESKTOP_DISTANCES
