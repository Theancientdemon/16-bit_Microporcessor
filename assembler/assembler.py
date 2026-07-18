# This is a assembler program for the microprocessor made by Darshan Suryawanshi Named "DSS 1601".
# This processor is simulation only.
# It uses mostly a instruction set based on RISC-V and various sudo instructions.

import sys
import os
import argparse
from repl import REPL
from tools import Options
from file_assembler import FileAssembler

def get_arg() -> argparse.Namespace:
    """Parse command line arguments and return them as a Namespace object."""
    parser = argparse.ArgumentParser(description="Assembler for DSS 1601 microprocessor.")
    parser.add_argument("input_file", nargs="?", 
                        help="""Input assembly file to be assembled.
                        If not provided, the assembler will run in REPL mode.""")
    parser.add_argument("output_file", nargs="?", 
                        help="""Output hex file to write the assembled code.
                        If not provided, the assembler will print the output to stdout.""")
    parser.add_argument("-lg", "--logisim", action="store_true", default=False, help="Generate Logisim compatible v3.0 hex addressed file.")
    parser.add_argument("-hx", "--hex", action="store_true", default=False, help="Generate Intel HEX file.")
    parser.add_argument("-m", "--mem", action="store_true", default=False, help="Generate verilog .mem file.")
    parser.add_argument("-p", "--print", action="store_true", default=False,
                        help="""Print the assembled code to stdout instead of writing to a file.
                        if both -p and -hx or -lg are used, the output will be printed as well as written to the specified output file.""")
    return parser.parse_args()

def parse_args() -> None:
    """Parse command line arguments and set the global options."""
    options = Options.get_options()
    args = get_arg()
    if args.input_file is None:
        options.repl = True
        return
    elif not os.path.isfile(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        sys.exit(1)
    else:
        options.input_file = args.input_file
        if args.output_file is None:
            options.write = False
            options.print = True
        else:
            options.write = True
        options.output_file = args.output_file
        
    if args.mem:
        options.filetype = "mem"
    elif args.hex:
        options.filetype = "hex"
    elif args.logisim:
        options.filetype = "logisim"
    else:
        options.filetype = "mem"  # Default to mem if no file type is specified
    if (args.logisim + args.hex + args.mem) > 1:
        print("Warning: Multiple file type options are specified. Only the mem format will be generated.")
    if args.print:
        options.print = True

def main() -> None:
    """Main function to run the assembler."""
    parse_args()
    options = Options.get_options()
    if options.repl:
        REPL.run()
    else:
        FileAssembler.assemble_file(options.input_file, options.output_file, options.filetype)
    
if __name__ == "__main__":
    main()
