from decoder import Decoder
from tools import Address, Label, Location, Options, Tools
import errors as Errors

class FileAssembler:
    @staticmethod
    def assemble_file(input_file: str, output_file: str | None, filetype: str) -> None:
        """Assemble the input file and write the output to the specified file."""
        options = Options.get_options()

        code = FileAssembler.get_assembled_code(input_file)

        if not code:
            print("File is empty.")
            return

        code, labels = FileAssembler.get_label_mapping(code)

        code = FileAssembler.set_Addresses(code, labels)

        if options.write:
            if filetype == "logisim":
                FileAssembler.write_logisim_file(output_file, code)
            elif filetype == "hex":
                FileAssembler.write_hex_file(output_file, code)
            elif filetype == "mem":
                FileAssembler.write_mem_file(output_file, code)
            else:
                raise Errors.FileTypeError(f"Unsupported file type: {filetype}")

        if options.print:
            FileAssembler.print_code(code)

    @staticmethod
    def set_Addresses(code:list[str|Address|Location], labels:dict[str, str]) -> list[str|Location]:
        new_code:list[str|Location] = []
        for word in code:
            if isinstance(word, Address):
                try:
                    word = labels[word.name]
                except KeyError:
                    Errors.PrintError(Errors.AddressError(f"Undefined address: {word.name}"),word.file, word.lineno )
            new_code.append(word)
        code = new_code
        return code

    @staticmethod
    def get_label_mapping(code:list[str|Label|Address|Location]) -> tuple[list[str|Address|Location], dict[str, str]]:
        index = 0
        Labels = {}
        newcode = []
        for word in code:
            if isinstance(word, Label):
                Labels[word.name] = Tools.hex(index)
                continue
            elif isinstance(word, Location):
                index = word.location
            else:
                index += 1
            newcode.append(word)
        return newcode, Labels

    @staticmethod
    def get_assembled_code(input_file: str) -> list[str|Label|Address|Location]:
        """Get the assembled code from the input file."""
        with open(input_file, 'r') as file:
                lines = file.readlines()
            
        code = []
        for lineno,line in enumerate(lines, 1):
            try:
                instructions = Decoder.decode(line.strip())
                if instructions is None:
                    continue
                if isinstance(instructions, str):
                    code.append(instructions)
                elif isinstance(instructions, (list, tuple)):
                    for instruction in instructions:
                        if isinstance(instruction, Address):
                            instruction.set_location(lineno, input_file)
                        code.append(instruction)
                else:
                    code.append(instructions)
            except Exception as e:
                Errors.PrintError(e, filename=input_file, lineno=lineno)
        return code

    @staticmethod
    def write_logisim_file(output_file: str, code: list) -> None:
        """Write the assembled code to a Logisim compatible file."""
        with open(output_file, 'w') as outfile:
            outfile.write("v3.0 hex addresses\n")
            index = 0
            for instruction in code:
                if isinstance(instruction, Location):
                    index = instruction.location
                    continue
                outfile.write(f"{index:04x} {instruction}\n")
                index += 1

    @staticmethod
    def write_hex_file(output_file: str, code: list) -> None:
        """Write the assembled code to an Intel HEX file."""
        raise NotImplementedError("HEX file output must be written")

    @staticmethod
    def write_mem_file(output_file: str, code: list) -> None:
        """Write the assembled code to a verilog .mem file."""
        with open(output_file, 'w') as outfile:
            index = 0
            for instruction in code:
                if isinstance(instruction, Location):
                    while index < instruction.location:
                        outfile.write(f"0000 ")
                        index += 1
                        if index % 8 == 0:
                            outfile.write("\n")
                    continue
                else:
                    outfile.write(f"{instruction} ")
                    index += 1
                    if index % 8 == 0:
                        outfile.write("\n")

    @staticmethod
    def print_code(code: list) -> None:
        """Print the assembled code to stdout."""
        for instruction in code:
            print(instruction)