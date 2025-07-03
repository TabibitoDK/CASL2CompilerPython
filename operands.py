"""
This file contains a comprehensive list of CASL II machine instruction opcodes,
their hexadecimal representation, and their length in memory words.
"""

OPCODE_MAP = {
    # Assembler Directives
    'START': ('', 0),
    'END':   ('', 0),
    'DS':    ('', 0),
    'DC':    ('', 1),

    # Machine Instructions from documentation
    # Data Transfer Instructions
    'LD':    ('10', 2),  # Load
    'ST':    ('11', 2),  # Store
    'LAD':   ('12', 2),  # Load Address

    # Arithmetic Instructions
    'ADDA':  ('20', 2),  # Add Arithmetic
    'SUBA':  ('21', 2),  # Subtract Arithmetic
    'ADDL':  ('22', 2),  # Add Logical
    'SUBL':  ('23', 2),  # Subtract Logical

    # Logical Instructions
    'AND':   ('30', 2),  # Logical AND
    'OR':    ('31', 2),  # Logical OR
    'XOR':   ('32', 2),  # Logical XOR

    # Comparison Instructions
    'CPA':   ('40', 2),  # Compare Arithmetic
    'CPL':   ('41', 2),  # Compare Logical

    # Shift Instructions
    'SLA':   ('50', 2),  # Shift Left Arithmetic
    'SRA':   ('51', 2),  # Shift Right Arithmetic
    'SLL':   ('52', 2),  # Shift Left Logical
    'SRL':   ('53', 2),  # Shift Right Logical

    # Branching Instructions
    'JUMP':  ('60', 2),  # Unconditional Jump
    'JPL':   ('61', 2),  # Jump on Plus
    'JMI':   ('62', 2),  # Jump on Minus
    'JNZ':   ('63', 2),  # Jump on Non-Zero
    'JZE':   ('64', 2),  # Jump on Zero
    'JOV':   ('65', 2),  # Jump on Overflow

    # Stack Instructions
    'PUSH':  ('70', 2),  # Push
    'POP':   ('71', 1),  # Pop

    # Subroutine Instructions
    'CALL':  ('80', 2),  # Call Subroutine
    'RET':   ('81', 1),  # Return from Subroutine

    # Other Instructions
    'SVC':   ('90', 2),  # Supervisor Call
    'NOP':   ('00', 1)   # No Operation
}

REGISTER_MAP = {f'GR{i}': i for i in range(8)}


