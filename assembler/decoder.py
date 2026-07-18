import codecs
from collections.abc import Generator
import os
from typing import Any
from tools import Address, Tools,Label,Location
import errors as Errors

class Decoder:

    registers = {
        "R0": "0",
        "ZERO": "0",
        "R1": "1",
        "RA": "1",
        "A" : "1",
        "R2": "2",
        "RB": "2",
        "B" : "2",
        "R3": "3",
        "RC": "3",
        "C" : "3",
        "R4": "4",
        "RD": "4",
        "D" : "4",
        "R5": "5",
        "RE": "5",
        "E" : "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "A",
        "Rtemp": "A",
        "R11": "B",
        "RADD": "B",
        "R12": "C",
        "RBP": "C",
        "BP" : "C",
        "R13": "D",
        "RRET": "D",
        "R14": "E",
        "RSP": "E",
        "SP": "E",
        "R15": "F",
        "RPC": "F",
        "PC": "F",
    }

    @staticmethod
    def get_token_generator(list_of_tokens:list[str]) -> Generator[str, Any, None]:
        for token in list_of_tokens:
            if token:
                yield token.upper()

    @staticmethod
    def get_next_token(tokens: Generator[str, Any, None], instruction:str) -> str:
        """Get the next token from the generator."""
        try:
            return next(tokens).strip().upper()
        except StopIteration:
            raise Errors.SyntaxError(f"Incomplete number of parameter for the \"{instruction}\" instruction.")

    @staticmethod
    def get_register(register: str) -> str:
        """Get the code for a register."""
        if register in Decoder.registers:
            return Decoder.registers[register]
        else:
            raise Errors.RegisterError(f"Invalid register: {register}")
        
    @staticmethod
    def decode(line: str) -> str|list[str|Label|Address|Location]:

        tokens = Decoder.get_token_generator(line.split())
        try:
            instruction = next(tokens)
        except StopIteration:
            return None
        
        match instruction.upper():
            case x if x.startswith("%"):
                raise None
            case x if x.startswith("#") or x.endswith(":"):
                return Label(instruction[1:] if instruction.startswith("#") else instruction[:-1])
            case x if x.startswith("$"):
                data = line[1:]
                code = []
                if data.startswith("[") or data.startswith("{"):
                    end = data.find("]" if data.startswith("[") else "}")
                    if end == -1:
                        raise Errors.SyntaxError("Missing closing bracket.")
                    data = data[1:end]
                    for item in data.split(",") if "," in data else data.split():
                        item = item.strip()
                        if item:
                            code.append(Tools.parse_address(item))
                    return code
                elif data.startswith("\""):
                    end = data.find("\"", 1)
                    if end == -1:
                        raise Errors.SyntaxError("Missing closing quote.")
                    data = data[1:end]
                    for char in codecs.decode(data, "unicode_escape"):
                        code.append(Tools.hex(ord(char)))
                    return code
                else:
                    return Tools.parse_address(data)
            case "ORG" | "ORIGIN" | "LOC" | "LOCATION":
                return Location(Tools.parse_number_int(Decoder.get_next_token(tokens, instruction)))
            case "IMPORT":
                from file_assembler import FileAssembler
                start = line.find("\"")
                if start == -1:
                    raise Errors.SyntaxError("Missing opening quote for import path.")
                end = line.find("\"", start + 1)
                if end == -1:
                    raise Errors.SyntaxError("Missing closing quote for import path.")
                path = line[start + 1:end]
                if not path:
                    raise Errors.SyntaxError("Import path cannot be empty.")
                if not os.path.isfile(path):
                    raise Errors.FileNotFoundError(f"File not found: {path}")
                return FileAssembler.get_assembled_code(path)
            case "NOP":
                return "0000"
            case "HLT" | "HALT":
                return "000F"
            case "ADD":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_next_token(tokens, instruction)
                if rs2.startswith("$"):
                    return "BA02",Tools.parse_number(rs2[1:]),f"1{rd}{rs1}A"
                else:
                    rs2 = Decoder.get_register(rs2)
                    return f"1{rd}{rs1}{rs2}"
            case "SUB":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_next_token(tokens, instruction)
                if rs2.startswith("$"):
                    return "BA02",Tools.parse_number(rs2[1:]),f"2{rd}{rs1}A"
                else:
                    rs2 = Decoder.get_register(rs2)
                    return f"2{rd}{rs1}{rs2}"
            case "AND":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_next_token(tokens, instruction)
                if rs2.startswith("$"):
                    return "BA02",Tools.parse_number(rs2[1:]),f"3{rd}{rs1}A"
                else:
                    rs2 = Decoder.get_register(rs2)
                    return f"3{rd}{rs1}{rs2}"
            case "OR":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_next_token(tokens, instruction)
                if rs2.startswith("$"):
                    return "BA02",Tools.parse_number(rs2[1:]),f"4{rd}{rs1}A"
                else:
                    rs2 = Decoder.get_register(rs2)
                    return f"4{rd}{rs1}{rs2}"
            case "XOR":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_next_token(tokens, instruction)
                if rs2.startswith("$"):
                    return "BA02",Tools.parse_number(rs2[1:]),f"5{rd}{rs1}A"
                else:
                    rs2 = Decoder.get_register(rs2)
                    return f"5{rd}{rs1}{rs2}"
            case "MOV" | "MOVE":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return f"8{rd}{rs}0"
            case "NOT":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs = Decoder.get_next_token(tokens, instruction)
                if rs.startswith("$"):
                    return "BA02",Tools.parse_number(rs2[1:]),f"6{rd}A0"
                else:
                    rs = Decoder.get_register(rs)
                    return f"6{rd}{rs}0"
            case "SLL" | "SHL" | "SHIFTL" |"SHIFTLEFT":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                count = Tools.parse_number_int(Decoder.get_next_token(tokens, instruction))
                if count < 0 or count > 15:
                    raise Errors.NumberError(f"Invalid shift count: {count}. Must be between 0 and 15.")
                return f"7{rd}{count:01x}0"
            case "SRL" |"SLR" | "SHR" | "SHIFTR" | "SHIFTRIGHT":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                count = Tools.parse_number_int(Decoder.get_next_token(tokens, instruction))
                if count < 0 or count > 15:
                    raise Errors.NumberError(f"Invalid shift count: {count}. Must be between 0 and 15.")
                return f"7{rd}{count:01x}1"
            case "SRA" | "SHIFTA" | "SHIFTARIGHT":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                count = Tools.parse_number_int(Decoder.get_next_token(tokens, instruction))
                if count < 0 or count > 15:
                    raise Errors.NumberError(f"Invalid shift count: {count}. Must be between 0 and 15.")
                return f"7{rd}{count:01x}2"
            case "LOAD":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                radd = Decoder.get_next_token(tokens, instruction)
                if radd.startswith("$"):
                    return f"B{rd}00",Tools.parse_address(radd[1:])
                else:
                    radd = Decoder.get_register(radd)
                    return f"9{rd}{radd}0"
            case "STORE":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                radd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return f"A{rs}{radd}0"
            case "PUSH":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return "BA00","0001","2EEA",f"A{rs}E0"
            case "POP":
                rd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return f"9{rd}E0","BA02","0001","1EEA"
            case "CALL" | "JAL":
                address = Decoder.get_next_token(tokens, instruction)
                try:
                    rret = Decoder.get_next_token(tokens, instruction)
                    if rret in Decoder.registers:
                        rret = Decoder.get_register(rret)
                    else:
                        rret = "D"
                except:
                    rret = "D"
                if address.startswith("$"):
                    return "BA02",Tools.parse_number(address[1:]),f"C{rret}A0"
                elif address in Decoder.registers:
                    address = Decoder.get_register(address)
                    return f"C{rret}{address}0"
                else:
                    return "BA02",Tools.parse_address(address),f"C{rret}A0"
            case "JUMP" | "JMP":
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return "BA02",Tools.parse_number(address[1:]),f"C0A0"
                elif address in Decoder.registers:
                    address = Decoder.get_register(address)
                    return f"C0{address}0"
                else:
                    return "BA02",Tools.parse_address(address),f"C0A0"
            case "BEQ" | "BE" | "JEQ" | "JE":
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs1}{rs2}0", Tools.parse_number(address[1:])
                else:
                    return f"D{rs1}{rs2}0", Tools.parse_address(address)
            case "BNE" | "JNE":
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs1}{rs2}1", Tools.parse_number(address[1:])
                else:
                    return f"D{rs1}{rs2}1", Tools.parse_address(address)
            case "BLT" | "JLT":
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs1}{rs2}2", Tools.parse_number(address[1:])
                else:
                    return f"D{rs1}{rs2}2", Tools.parse_address(address)
            case "BGT" | "JGT":
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs1}{rs2}3", Tools.parse_number(address[1:])
                else:
                    return f"D{rs1}{rs2}3", Tools.parse_address(address)
            case "BLE" | "JLE":
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs1}{rs2}4", Tools.parse_number(address[1:])
                else:
                    return f"D{rs1}{rs2}4", Tools.parse_address(address)
            case "BGE" | "JGE":
                rs1 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                rs2 = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs1}{rs2}5", Tools.parse_number(address[1:])
                else:
                    return f"D{rs1}{rs2}5", Tools.parse_address(address)
            case "BM" | "BS" | "BNEG" | "JM" | "JS" | "JNEG":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return "BA02","8000",f"f3AA{rs}",f"DA01", Tools.parse_number(address[1:])
                else:
                    return "BA02","8000",f"3AA{rs}",f"DA01", Tools.parse_address(address)
            case "BP" | "JP" | "BNS" | "JNS" | "BPOS" | "JPOS":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return "BA02","8000",f"3AA{rs}",f"DA00", Tools.parse_number(address[1:])
                else:
                    return "BA02","8000",f"3AA{rs}",f"DA00", Tools.parse_address(address)
            case "BZ" | "JZ":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs}00", Tools.parse_number(address[1:])
                else:
                    return f"D{rs}00", Tools.parse_address(address)
            case "BNZ" | "JNZ":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                address = Decoder.get_next_token(tokens, instruction)
                if address.startswith("$"):
                    return f"D{rs}01", Tools.parse_number(address[1:])
                else:
                    return f"D{rs}01", Tools.parse_address(address)
            case "INC":
                r = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return "BA02","0001",f"1{r}{r}A"
            case "DCR":
                r = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return "BA02","0001",f"2{r}{r}A"
            case "RET" | "RETURN":
                try:
                    r = Decoder.get_next_token(tokens, instruction)
                except:
                    return "C0D0"
                else:
                    return f"C0{Decoder.get_register(r)}0"
            case "OUT":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                radd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return f"F{rs}{radd}0"
            case "IN":
                rs = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                radd = Decoder.get_register(Decoder.get_next_token(tokens, instruction))
                return f"E{rs}{radd}0"
            case _:
                raise Errors.UnknownInstructionError(f"\"{instruction}\" is not a valid instruction.")
        