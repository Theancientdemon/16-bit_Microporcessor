import errors as Errors
import codecs

class Tools:
    @staticmethod
    def hex(data: int) -> str:
        return data.__format__("04x")
    
    @staticmethod
    def bin(data: int) -> str:
        return f"{data & 0xFFFF :016b}"
    
    @staticmethod
    def signed_bin_to_int(bin_str: str) -> int:
        val = int(bin_str, 2)
        if bin_str[0] == '1':  # if sign bit is 1, it's negative
            val -= (1 << len(bin_str))
        return val
    
    @staticmethod
    def oct(data: int) -> str:
        return data.__format__("o")
    
    @staticmethod
    def parse_number_int(value: str) -> int:
        try: 
            return int(value, 0)
        except ValueError:
            try:
                match value[-1].upper():
                    case "H":
                        return int(value[:-1], 16)
                    case "B":
                        return int(value[:-1], 2)
                    case "S":
                        return Tools.signed_bin_to_int(value[:-1])
                    case "D":
                        return int(value[:-1])
                    case "O":
                        return int(value[:-1], 8)
                    case _:
                        raise Errors.NumberError(f"Invalid number format for \"{value}\"")
            except ValueError:
                raise Errors.NumberError(f"Invalid number \"{value}\" for respective format")
    
    @staticmethod
    def parse_number(value: str) -> str:
        return Tools.hex(Tools.parse_number_int(value))
    
    @staticmethod
    def parse_address(value: str) -> str:
        if value.startswith("@"):
            return Address(value[1:])
        elif value.startswith("\""):
            value = codecs.decode(value[1:-1], "unicode_escape")
            if len(value) == 1:
                return Tools.hex(ord(value))
            elif len(value) == 2:
                return Tools.hex(ord(value[0]) << 8 | ord(value[1]))
            else:
                raise Errors.NumberError(f"character literal \"{value}\" is too long for a single word")
        else:
            return Tools.parse_number(value)

class Address:
    def __init__(self, address: str):
        self.name = address
        self.lineno = None
        self.file = None
    
    def set_location(self, lineno: int, file: str):
        self.lineno = lineno
        self.file = file

    def __str__(self) -> str:
        return f"address: {self.name}"

class Label:
    def __init__(self, label: str):
        self.name = label

    def __str__(self) -> str:
        return f"label: {self.name}"

class Location:
    def __init__(self, location: int):
        self.location = location
    
    def __str__(self) -> str:
        return f"location: {self.location:04x}"

class Options:
    """Class to hold global options for the assembler."""
    global_options_instance = None
    def __init__(self):
        self.input_file: str | None = None
        self.output_file: str | None = None
        self.filetype: str | None = None
        self.print: bool = False
        self.write: bool = False
        self.repl: bool = False

    @staticmethod
    def get_options() -> "Options":
        """Singleton method to get the global options instance."""
        if Options.global_options_instance is None:
            Options.global_options_instance = Options()
        return Options.global_options_instance
