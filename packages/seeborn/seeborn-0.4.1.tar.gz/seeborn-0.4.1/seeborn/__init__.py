from .code_manager import CodeExample
from .built_in_examples import load_built_in_examples
from .examples_viewer import get_example, copy_example

_code_instance = CodeExample()
load_built_in_examples(_code_instance)

def snss(name):
    """Print a code example by name."""
    print(_code_instance(name))

def gr_1():
    """Display the gr_1 example code"""
    print(get_example('gr_1'))

def gr_2():
    """Display the gr_2 example code"""
    print(get_example('gr_2'))

def gr_3():
    """Display the gr_3 example code"""
    print(get_example('gr_3'))

def gr_4():
    """Display the gr_4 example code"""
    print(get_example('gr_4'))

def show_code(example_name):
    """
    Display a code example by name.
    
    Args:
        example_name (str): Name of the example to display
    """
    print(get_example(example_name))

def c(example_name):
    """
    Copy a code example to clipboard without displaying it.
    
    Args:
        example_name (str): Name of the example to copy
    
    Returns:
        bool: True if copying was successful, False otherwise
    """
    success = copy_example(example_name)
    if success:
        print(f"Code example '{example_name}' has been copied to clipboard!")
    return success
