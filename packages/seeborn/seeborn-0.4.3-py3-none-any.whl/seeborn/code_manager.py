import os

class CodeExample:
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), 'examples')
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def save_code(self, name, code):
        """Save a code example to a text file."""
        file_path = os.path.join(self.base_path, f"{name}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
    
    def get_code(self, name):
        """Retrieve a code example by name."""
        file_path = os.path.join(self.base_path, f"{name}.txt")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Code example '{name}' not found."
    
    def __getattr__(self, name):
        """Allow accessing code examples as attributes."""
        return self.get_code(name)
    
    def __str__(self):
        """Allow printing the code example directly."""
        return self.get_code(self._current_name)
    
    def __call__(self, name):
        """Allow using the instance as a function call."""
        self._current_name = name
        return self
