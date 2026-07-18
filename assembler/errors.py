import sys

class NumberError(ValueError):
    """Exception raised for errors in the number format."""
    pass

class RegisterError(ValueError):
    """Exception raised for errors in the register format."""
    pass

class SyntaxError(SyntaxError):
    """Exception raised for syntax errors in the assembly code."""
    pass

class NOOperation(Exception):
    """Signifies that the current line should be ignored."""
    pass

class UnknownInstructionError(Exception):
    """Exception raised for unknown instructions in the assembly code."""
    pass

class FileNotFoundError(IOError):
    """Exception raised when the specified file is not found."""
    pass

class FileTypeError(Exception):
    """Exception raised for unsupported file types."""
    pass

class AddressError(Exception):
    """Exception raised for errors when a Label is not found for a particular address."""
    pass

def PrintError(error, filename:str|None = None, lineno:int|None = None, *, exit:bool = True) -> None:
    """Print an error message."""
    if filename and lineno:
        print(f"\033[31mError in {filename} at line {lineno}:\033[0m")
    elif filename:
        print(f"\033[31mError in {filename}:\033[0m")
    elif lineno:
        print(f"\033[31mError at line {lineno}:\033[0m")
    else:
        print("\033[31mError:\033[0m")
    print(f"\033[31m{error.__class__.__name__}\033[0m")
    print("\t", error)
    # raise error
    if exit:
        sys.exit(1)