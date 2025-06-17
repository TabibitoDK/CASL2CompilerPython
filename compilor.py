import re


import re

class Compiler:
    """
    A two-pass assembler for the CASL II language.
    """
    def __init__(self):
        self.symbol_table = {} 
        self.intermediate_representation = []
        self.machine_code = []
        self.start_address = 0

        # --- THIS IS THE KEY CHANGE ---
        # A complete, centralized map of all opcodes and their properties.
        # This now belongs to the compiler instance (self).
        # Format: {mnemonic: (hex_opcode, length_in_words)}
        self.OPCODE_MAP = {
            'START': ('', 0),
            'END':   ('', 0),
            'DS':    ('', 0),  # Length is variable, handled in first_pass
            'DC':    ('', 1),  # Length is variable, handled in first_pass
            'LD':    ('10', 2),
            'ADDA':  ('30', 2), # Using a placeholder hex value for ADDA
            'ST':    ('11', 2),
            'JUMP':  ('60', 2), # Using a placeholder hex value for JUMP
            'RET':   ('81', 1),
            'NOP':   ('00', 1)
        }

    def compile(self, source_code):
        """
        Main method to orchestrate the entire compilation process.
        """
        print("--- Starting Compilation ---")
        try:
            # We will define these methods in the upcoming steps.
            self.first_pass(source_code)
            print("\n--- First Pass Complete ---")
            print("Symbol Table:", self.symbol_table)

            self.second_pass()
            print("\n--- Second Pass Complete ---")
            print("Generated Machine Code:", self.machine_code)

            return self.machine_code
        except Exception as e:
            print(f"Compilation Error: {e}")
            return None

    def _parse_line(self, line):
            original_line = line
            
            # Clean the line: remove leading/trailing whitespace and comments.
            line = line.strip()
            if not line or line.startswith(';'):
                return None
            if ';' in line:
                line = line.split(';', 1)[0].strip()

            # Split the line into the first word and the rest of the line
            parts = line.split(None, 1)
            first_word = parts[0]

            label, opcode, operands_str = None, None, ''

            # --- THE NEW, ROBUST LOGIC ---
            # Is the first word on the line a known opcode?
            if first_word in self.OPCODE_MAP:
                # YES: Then there is no label.
                opcode = first_word
                if len(parts) > 1:
                    operands_str = parts[1]
            else:
                # NO: Then the first word must be a label.
                label = first_word
                if len(parts) < 2:
                    raise ValueError(f"Labeled line '{label}' is missing its instruction.")
                
                # The rest of the line contains the opcode and operands
                rest_of_line = parts[1]
                opcode_and_operands = rest_of_line.split(None, 1)
                opcode = opcode_and_operands[0]
                if len(opcode_and_operands) > 1:
                    operands_str = opcode_and_operands[1]

            # Final validation that we found a valid opcode
            if opcode not in self.OPCODE_MAP:
                raise ValueError(f"Unknown opcode '{opcode}' on line: '{original_line.strip()}'")

            operands = [op.strip() for op in operands_str.split(',')] if operands_str else []
            return {'label': label, 'opcode': opcode, 'operands': operands}

    def first_pass(self, source_code):
        location_counter = 0
        lines = source_code.split('\n')

        # This is a partial map of opcodes to their properties. You will need to
        # fill this out completely for the final compiler.
        # Format: {mnemonic: (hex_opcode, length_in_words)}
        
        for line in lines:
            parsed = self._parse_line(line) # Assume _parse_line from Step 2 exists and works
            if not parsed:
                continue

            # Before we do anything else, we save the parsed line along with its calculated
            # address. This is our intermediate representation.
            parsed['address'] = location_counter
            self.intermediate_representation.append(parsed)

            if parsed['label']:
                if parsed['label'] in self.symbol_table:
                    # It's an error if the same label is defined twice.
                    raise NameError(f"Duplicate label definition: '{parsed['label']}'")
                # This is where you add the new label and its address to the symbol table.
                self.symbol_table[parsed["label"]] = location_counter# FILL IN THE BLANK (How do you add a key-value pair to a dictionary?)

            opcode = parsed['opcode']
            if opcode in self.OPCODE_MAP:
                # This logic correctly increments the location counter based on the instruction type.
                if opcode == 'DS':
                    # DS (Define Storage) reserves a block of memory. The size is given by its operand.
                    size = int(parsed['operands'][0])
                    location_counter += size
                elif opcode == 'DC':
                    # DC (Define Constant) creates one word for each constant listed.
                    location_counter += len(parsed['operands'])
                else:
                    # For most other instructions, the length is fixed. We look it up in our map.
                    _, length = self.OPCODE_MAP[opcode]
                    location_counter += length
            elif opcode != 'START' and opcode != 'END':
                raise ValueError(f"Unknown opcode: '{opcode}'")
    def second_pass(self):
        REGISTER_MAP = {'GR1': 1}

        for instruction in self.intermediate_representation:
            opcode = instruction['opcode']
            operands = instruction['operands']

            if opcode in ['START', 'END', 'DS']:
                continue
            
            if opcode == 'LD':
                op_hex, _ = self.OPCODE_MAP[opcode]
                r1_val = REGISTER_MAP[operands[0]]
                address_operand = operands[1]

                # We look up the address by using the label string (address_operand)
                # as the key in our completed symbol_table dictionary.
                address = self.symbol_table[address_operand]
                
                first_word = f"{op_hex}{r1_val}{0}"
                
                # An f-string with the format specifier ':04X' is perfect for this.
                # X -> Convert to uppercase Hexadecimal.
                # 4 -> Ensure the output is 4 characters wide.
                # 0 -> Pad with leading zeros if necessary.
                # e.g., the number 6 becomes "0006"
                second_word = f"{address:04X}"
                self.machine_code.append(first_word)
                self.machine_code.append(second_word)


if __name__ == "__main__":
    casl_program = """
    PGM     START
            LD    GR1,A      ; Load value at address A into GR1
            ADDA  GR1,B      ; Add value at address B to GR1
            ST    GR1,C      ; Store the result from GR1 into address C
    A       DC    3          ; Define constant A with value 3
    B       DC    5          ; Define constant B with value 5
    C       DS    1          ; Reserve 1 word of storage for C
            END                ; End of the program
    """
    # Create an instance of the class by calling its name like a function.
    compiler = Compiler()
        
    # Call the compile method on the 'compiler' object, passing the source code as an argument.
    compiler.compile(casl_program)
