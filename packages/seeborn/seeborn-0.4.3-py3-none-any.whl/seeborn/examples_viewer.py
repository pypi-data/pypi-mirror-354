import os
import pyperclip
from .code_manager import CodeExample

def get_example(example_name):
    """
    Get and display a code example by name.
    
    Args:
        example_name (str): Name of the example to display
    
    Returns:
        str: The code example text
    """
    manager = CodeExample()
    return manager.get_code(example_name)

def copy_example(example_name):
    """
    Copy a code example to clipboard without displaying it.
    
    Args:
        example_name (str): Name of the example to copy
    
    Returns:
        bool: True if copying was successful, False otherwise
    """
    try:
        manager = CodeExample()
        code = manager.get_code(example_name)
        try:
            pyperclip.copy(code)
            return True
        except pyperclip.PyperclipException:
            try:
                # Try using Windows clipboard specifically
                import win32clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(code)
                win32clipboard.CloseClipboard()
                return True
            except:
                print("Could not copy to clipboard. Please make sure you have pywin32 installed.")
                print("You can install it using: pip install pywin32")
                return False
    except Exception as e:
        print(f"Error getting code example: {str(e)}")
        return False

def get_example_by_name(example_name):
    """
    Get the code for a specific example by its name (e.g., 'gr_1', 'gr_2', etc.)
    """
    # Get the directory where the examples are stored
    current_dir = os.path.dirname(os.path.abspath(__file__))
    examples_dir = os.path.join(current_dir, 'examples')
    
    # Read all example files
    example_files = ['gradio_examples.txt']
    
    for file_name in example_files:
        file_path = os.path.join(examples_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split content by '##' to get individual examples
            examples = content.split('##')
            
            # Find the requested example
            for example in examples:
                if example.strip().startswith(example_name):
                    return example.strip()
                    
        except FileNotFoundError:
            continue
            
    return f"Example '{example_name}' not found." 