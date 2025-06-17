import re

class Compiler:
    """
    A two-pass assembler for a subset of the CASL II language.
    This assembler builds a symbol table in the first pass and generates
    machine code in the second pass.
    """
    def __init__(self):
        """Initializes the compiler's state."""
        self.symbol_table = {}
        self.intermediate_representation = []
        self.machine_code = []
        self.start_address = 0

        # Defines the properties of each recognized machine instruction and directive.
        # Format: {mnemonic: (hex_opcode, length_in_words)}
        self.OPCODE_MAP = {
            # Assembler Directives
            'START': ('', 0),
            'END':   ('', 0),
            'DS':    ('', 0),  # Length is variable, handled in first_pass
            'DC':    ('', 1),  # Length is variable, handled in first_pass

            # Machine Instructions
            'LD':    ('10', 2),
            'ST':    ('11', 2),
            'ADDA':  ('30', 2),
            'JUMP':  ('60', 2),
            'RET':   ('81', 1),
            'NOP':   ('00', 1)
        }

        # Maps opcodes to their corresponding handler function for the second pass.
        # This allows for modular processing of different instruction formats.
        self.instruction_handlers = {
            # Format: OPCODE r, adr
            'LD': self._handle_format_r_adr,
            'ST': self._handle_format_r_adr,
            'ADDA': self._handle_format_r_adr,

            # Format: OPCODE adr
            'JUMP': self._handle_format_adr,

            # Format: No operands
            'RET': self._handle_no_operand,
            'NOP': self._handle_no_operand,
            
            # Special Directives
            'DC': self._handle_dc
        }
        
        # Maps general register names to their 4-bit numeric representation.
        self.REGISTER_MAP = {f'GR{i}': i for i in range(8)}

    def compile(self, source_code):
        """
        Orchestrates the two-pass compilation process.
        
        Args:
            source_code (str): The CASL II source code to compile.

        Returns:
            A list of strings representing the machine code, or None on error.
        """
        print("--- Starting Compilation ---")
        try:
            # First pass: Build symbol table and intermediate representation.
            self.first_pass(source_code)
            print("\n--- First Pass Complete ---")
            print("Symbol Table:", self.symbol_table)

            # Second pass: Generate machine code from the intermediate representation.
            self.second_pass()
            print("\n--- Second Pass Complete ---")
            print("Generated Machine Code:", self.machine_code)

            return self.machine_code
        except (ValueError, NameError) as e:
            print(f"Compilation Error: {e}")
            return None

    def _parse_line(self, line):
        """
        Parses a single line of assembly code into its components.
        
        Returns:
            A dictionary {'label': str|None, 'opcode': str, 'operands': list} or None.
        """
        original_line = line
        
        # Remove comments and leading/trailing whitespace.
        line = line.strip()
        if not line or line.startswith(';'):
            return None
        if ';' in line:
            line = line.split(';', 1)[0].strip()

        parts = line.split(None, 1)
        first_word = parts[0]
        label, opcode, operands_str = None, None, ''

        # Determine if the line contains a label.
        # If the first word is not a known opcode, it must be a label.
        if first_word in self.OPCODE_MAP:
            opcode = first_word
            if len(parts) > 1:
                operands_str = parts[1]
        else:
            # The first word is a label.
            label = first_word
            if len(parts) < 2:
                raise ValueError(f"Labeled line '{label}' is missing its instruction.")
            
            rest_of_line = parts[1]
            opcode_and_operands = rest_of_line.split(None, 1)
            opcode = opcode_and_operands[0]
            if len(opcode_and_operands) > 1:
                operands_str = opcode_and_operands[1]

        # Ensure a valid opcode was identified.
        if opcode not in self.OPCODE_MAP:
            raise ValueError(f"Unknown opcode '{opcode}' on line: '{original_line.strip()}'")

        # Split operands string by comma into a list.
        operands = [op.strip() for op in operands_str.split(',')] if operands_str else []
        return {'label': label, 'opcode': opcode, 'operands': operands}

    def first_pass(self, source_code):
        """
        Processes the source code to build the symbol table and intermediate representation.
        The location counter is updated based on instruction and directive lengths.
        """
        location_counter = 0
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines):
            parsed = self._parse_line(line)
            if not parsed:
                continue

            # Store the parsed instruction with its memory address for the second pass.
            parsed['address'] = location_counter
            self.intermediate_representation.append(parsed)

            # If a label exists, add it to the symbol table with the current address.
            if parsed['label']:
                if parsed['label'] in self.symbol_table:
                    raise NameError(f"Duplicate label definition: '{parsed['label']}'")
                self.symbol_table[parsed["label"]] = location_counter

            # Increment location counter based on instruction or directive.
            opcode = parsed['opcode']
            if opcode in self.OPCODE_MAP:
                if opcode == 'DS':
                    # DS reserves a block of memory specified by the operand.
                    size = int(parsed['operands'][0])
                    location_counter += size
                elif opcode == 'DC':
                    # DC reserves one word for each constant defined.
                    location_counter += len(parsed['operands'])
                else:
                    # For standard instructions, get the length from the opcode map.
                    _, length = self.OPCODE_MAP[opcode]
                    location_counter += length
            elif opcode != 'START' and opcode != 'END':
                # This check is redundant if _parse_line is correct, but serves as a safeguard.
                raise ValueError(f"Unknown opcode: '{opcode}'")

    def second_pass(self):
        """
        Generates machine code by iterating through the intermediate representation.
        Uses the completed symbol table to resolve addresses.
        """
        self.machine_code = [] # Ensure list is empty before starting
        for instruction in self.intermediate_representation:
            opcode = instruction['opcode']

            # Skip directives that do not generate code.
            if opcode in ['START', 'END', 'DS']:
                continue
            
            # Delegate to the appropriate handler based on the opcode.
            handler = self.instruction_handlers.get(opcode)
            if handler:
                handler(instruction)
            else:
                # This warning helps identify which instructions lack a generation handler.
                print(f"Warning: Second pass handler for opcode '{opcode}' is not yet implemented.")

    def _handle_format_r_adr(self, instruction):
        """
        Generates code for instructions like 'LD r, adr'.
        Format: [Opcode][r][x] [Address]
        """
        op_hex = self.OPCODE_MAP[instruction['opcode']][0]
        operands = instruction['operands']
        
        r_val = self.REGISTER_MAP[operands[0]]
        address = self.symbol_table[operands[1]]
        x_val = 0 # Index register is not implemented, default to 0.
        
        # Construct the two words of machine code.
        first_word = f"{op_hex}{r_val}{x_val}"
        second_word = f"{address:04X}" # Format address as 4-digit uppercase hex.
        self.machine_code.extend([first_word, second_word])

    def _handle_format_adr(self, instruction):
        """
        Generates code for instructions like 'JUMP adr'.
        Format: [Opcode][r][x] [Address], where r is 0.
        """
        op_hex = self.OPCODE_MAP[instruction['opcode']][0]
        operands = instruction['operands']
        
        address = self.symbol_table[operands[0]]
        r_val = 0 # The 'r' field is unused in this format.
        x_val = 0 # Index register is not implemented, default to 0.
        
        # Construct the two words of machine code.
        first_word = f"{op_hex}{r_val}{x_val}"
        second_word = f"{address:04X}"
        self.machine_code.extend([first_word, second_word])

    def _handle_no_operand(self, instruction):
        """
        Generates code for single-word instructions like 'RET'.
        Format: [Opcode][r][x], where r and x are 0.
        """
        op_hex = self.OPCODE_MAP[instruction['opcode']][0]
        
        # Construct the single word of machine code.
        machine_word = f"{op_hex}00" # r and x fields are zero.
        self.machine_code.append(machine_word)

    def _handle_dc(self, instruction):
        """
        Generates code for the 'DC' (Define Constant) directive.
        """
        for const in instruction['operands']:
            # TODO: Extend to handle hex ('#FFFF') and string constants.
            value = int(const)
            # Format constant as a 16-bit (4-digit hex) machine word.
            machine_word = f"{value:04X}"
            self.machine_code.append(machine_word)


if __name__ == "__main__":
    # Example CASL II program for demonstration and testing.
    casl_program = """
    PGM      START
             LD    GR1,A      ; Load value at address A into GR1
             ADDA  GR1,B      ; Add value at address B to GR1
             ST    GR1,C      ; Store the result from GR1 into address C
    A        DC    3          ; Define constant A with value 3
    B        DC    5          ; Define constant B with value 5
    C        DS    1          ; Reserve 1 word of storage for C
             END              ; End of the program
    """
    # Instantiate and run the compiler.
    compiler = Compiler()
    compiler.compile(casl_program)