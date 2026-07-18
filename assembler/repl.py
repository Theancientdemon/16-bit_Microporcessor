import sys
from decoder_1601 import Decoder
from tools1601 import Tools
import errors1601 as Errors

class REPL:
    @staticmethod
    def run():
        print("REPL for DSS 1601 Assembler. Type 'exit' to quit. Type 'help' for commands.")
        while True:
            try:
                line = input("\033[34m>>> \033[0m").strip()
                if not line:
                    continue
                ins_parts = line.split()
                match ins_parts[0].upper():
                    case "EXIT" | "QUIT":
                        print("Exiting REPL.")
                        sys.exit(0)
                    case "HELP" | "?":
                        if len(ins_parts) > 1:
                            REPL.get_help(ins_parts[1])
                        else:
                            REPL.get_help()
                        continue
                    case "BIN" | "BINARY":
                        code = [Tools.bin(int(Tools.parse_number(number), 16)) for number in ins_parts[1:]]
                    case "HEX" | "HEXADECIMAL":
                        code = [Tools.parse_number(number) for number in ins_parts[1:]]
                    case "DEC" | "INT":
                        code = [Tools.parse_number_int(number) for number in ins_parts[1:]]
                    case "OCT" | "OCTAL":
                        code = [Tools.oct(Tools.parse_number_int(number)) for number in ins_parts[1:]]
                    case _:
                        code = Decoder.decode(line)

                if code is not None:
                    REPL.print_code(code)
            
            except (EOFError, KeyboardInterrupt):
                print("\n\033[35mExiting REPL.\033[0m")
                sys.exit(0)
            except Exception as e:
                Errors.PrintError(e,exit=False)
    
    @staticmethod
    def get_help(obj=None):
        if obj is None:
            print("Usage: <HELP | ?> <COMMAND>")
            print("Prints the help for the specified command.")
            print("type \'list\' for list of commands.")
        else:
            match obj.upper():
                case "LIST":
                    REPL.print_command_list()
                case "$":
                    print("$ <value> ... : Immediate values in hexadecimal format.")
                    print("$[<value> ...] : List / Array of immediate values in hexadecimal format.")
                    print("$\"<string>\" : Array of hexadecimal values representing each character in the string in ascii format.")
                case "EXIT" | "QUIT":
                    print("EXIT | QUIT : Exit the REPL.")
                case "BIN" | "BINARY":
                    print("BIN <number> ... : Convert numbers to binary format.")
                case "HEX" | "HEXADECIMAL":
                    print("HEX <number> ... : Convert numbers to hexadecimal format.")
                case "DEC" | "INT":
                    print("DEC <number> ... : Convert numbers to decimal format.")
                case "OCT" | "OCTAL":
                    print("OCT <number> ... : Convert numbers to octal format.")
                case "ADD":
                    print("ADD <Register destination> <Register source 1> <Register source 2 | Immediate value> : Arithmetic addition.")
                case "SUB":
                    print("SUB <Register destination> <Register source 1> <Register source 2 | Immediate value> : Arithmetic subtraction.")
                case "MUL":
                    print("MUL | MULTIPLY : Multiply RA | R1 with RB | R2 and store the result in [RA : RB].")
                case "DIV":
                    print("DIV | DIVIDE : Divide [RA : RB] by RC | R3 and store the Quotient in RA | R1 and the remainder in RB | R2.")
                case "AND":
                    print("AND <Register destination> <Register source 1> <Register source 2 | Immediate value> : Bitwise AND operation.")
                case "OR":
                    print("OR <Register destination> <Register source 1> <Register source 2 | Immediate value> : Bitwise OR operation.")
                case "XOR":
                    print("XOR <Register destination> <Register source 1> <Register source 2 | Immediate value> : Bitwise XOR operation.")
                case "NOT":
                    print("NOT <Register destination> <Register source | Immediate value> : Bitwise NOT operation.")
                case "SHL":
                    print("SHL <Register> <Count> : Bitwise shift left operation.")
                case "SHR":
                    print("SHR <Register> <Count> : Bitwise shift right operation.")
                case "SRA":
                    print("SRA <Register> <Count> : Bitwise arithmetic shift right operation.")
                case "CMP":
                    print("CMP <Register source 1> <Register source 2 | Immediate value> : Compare two values.")
                case "JMP":
                    print("JMP <Address> : Jump to a specified address.")
                case "CALL":
                    print("CALL | JAL <Address> : Call a subroutine at a specified address.")
                case "RET":
                    print("RET : Return from a subroutine.")
                case "PUSH":
                    print("PUSH <Register> : Push a value onto the stack.")
                case "POP":
                    print("POP <Register> : Pop a value from the stack.")
                case "LOAD":
                    print("LOAD <Register destination> <Register address | Immediate value> : Load a value from memory.")
                case "STORE":
                    print("STORE <Register source> <Register address> : Store a value in memory.")
                case "BNE" | "BEQ" | "BLT" | "BGT" | "BLE" | "BGE":
                    print(f"""B<condition> <Address> : Conditional branch.
                          Conditions:
                          BNE : Branch if Not Equal.
                          BEQ : Branch if Equal.
                          BLT : Branch if Less Than.
                          BGT : Branch if Greater Than.
                          BLE : Branch if Less Than or Equal.
                          BGE : Branch if Greater Than or Equal.
                          BZ : Branch if Zero.
                          BNZ : Branch if Not Zero.
                          BPOS : Branch if Positive.
                          BNEG : Branch if Negative.
                          BOV : Branch if Overflow.
                          BNO : Branch if Not Overflow.
                          BC : Branch if Carry Set.
                          BNC : Branch if Carry Clear.""")
                case "NOP":
                    print("NOP : No operation (does nothing). Stalls the CPU for one cycle.")
                case "HLT":
                    print("HLT : Halt the execution of the program. Stops the CPU until reset.")
                case _:
                    print(f"No help available for command '{obj}'.")

    @staticmethod
    def print_command_list():
        print("Available commands:")
        print("'$' : Imediate values in hexadecimal format.")#
        print("BIN | BINARY : Convert numbers to binary format.")#
        print("HEX | HEXADECIMAL : Convert numbers to hexadecimal format.")#
        print("DEC | INT : Convert numbers to decimal format.")#
        print("OCT | OCTAL : Convert numbers to octal format.")#
        print("EXIT | QUIT : Exit the REPL.")#
        print("HELP | ? : Show this help message or help for a specific command.")#
        print("ADD : Arithmetic addition.")
        print("SUB : Arithmetic subtraction.")
        print("MUL : Arithmetic multiplication.")
        print("DIV : Arithmetic division.")
        print("AND : Bitwise AND operation.")
        print("OR : Bitwise OR operation.")
        print("XOR : Bitwise XOR operation.")
        print("NOT : Bitwise NOT operation.")
        print("SHL : Bitwise shift left operation.")
        print("SHR : Bitwise shift right operation.")
        print("SRA : Bitwise arithmetic shift right operation.")
        print("CMP : Compare two values.")
        print("JMP : Jump to a specified address.")
        print("CALL : Call a subroutine at a specified address.")
        print("RET : Return from a subroutine.")
        print("PUSH : Push a value onto the stack.")
        print("POP : Pop a value from the stack.")
        print("LOAD : Load a value from memory.")
        print("STORE : Store a value in memory.")
        print("B<condition> : Conditional branch (e.g., BEQ, BNE, BLT, BGT, BLE, BGE).")
        print("NOP : No operation (does nothing).")
        print("HLT : Halt the execution of the program.")
           
    @staticmethod
    def print_code(code: str | list[str]) -> None:
        """Print the code in a formatted way."""
        print("\033[36m",end="")
        if isinstance(code, list):
            for byte in code:
                print(byte, end=' ')
            print()  # Newline after printing all bytes
        else:
            print(code)
            