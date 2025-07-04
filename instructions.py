# instructions.py
# This file contains the execution logic for each COMET II instruction.

def ld_reg(simulator, r1, r2):
    """Executes LD r1, r2 (Register-to-Register Load)"""
    simulator.gr[r1] = simulator.gr[r2]
    simulator._update_flags(simulator.gr[r1])
    if simulator.debug:
        print(f"  EXECUTING: LD GR{r1}, GR{r2} -> GR{r1} = {simulator.gr[r1]}")

def ld_mem(simulator, r, x):
    """Executes LD r, addr, x (Memory-to-Register Load)"""
    addr_word = simulator._fetch()
    effective_address = simulator._get_effective_address(r, x, addr_word)
    
    # Ensure we don't read past memory bounds
    if 0 <= effective_address < simulator.MEMORY_SIZE:
        simulator.gr[r] = simulator.memory[effective_address]
        simulator._update_flags(simulator.gr[r])
        if simulator.debug:
            print(f"  EXECUTING: LD GR{r}, mem[{effective_address:04X}] -> GR{r} = {simulator.gr[r]}")
    else:
        print(f"Error: Memory read out of bounds at address {effective_address:04X}")
        simulator.is_running = False

def st(simulator, r, x):
    """Executes ST r, addr, x (Store)"""
    addr_word = simulator._fetch()
    effective_address = simulator._get_effective_address(r, x, addr_word)
    
    if 0 <= effective_address < simulator.MEMORY_SIZE:
        simulator.memory[effective_address] = simulator.gr[r]
        if simulator.debug:
            print(f"  EXECUTING: ST GR{r}, mem[{effective_address:04X}] -> mem[{effective_address:04X}] = {simulator.gr[r]}")
    else:
        print(f"Error: Memory write out of bounds at address {effective_address:04X}")
        simulator.is_running = False

def lad(simulator, r, x):
    """Executes LAD r, addr, x (Load Address)"""
    addr_word = simulator._fetch()
    effective_address = simulator._get_effective_address(r, x, addr_word)
    simulator.gr[r] = effective_address
    simulator._update_flags(simulator.gr[r])
    if simulator.debug:
        print(f"  EXECUTING: LAD GR{r}, {effective_address:04X} -> GR{r} = {simulator.gr[r]}")

def adda_reg(simulator, r1, r2):
    """Executes ADDA r1, r2 (Register-to-Register Add)"""
    simulator.gr[r1] += simulator.gr[r2]
    simulator._update_flags(simulator.gr[r1])
    if simulator.debug:
        print(f"  EXECUTING: ADDA GR{r1}, GR{r2} -> GR{r1} = {simulator.gr[r1]}")

def adda_mem(simulator, r, x):
    """Executes ADDA r, addr, x (Memory-to-Register Add)"""
    addr_word = simulator._fetch()
    effective_address = simulator._get_effective_address(r, x, addr_word)
    
    if 0 <= effective_address < simulator.MEMORY_SIZE:
        simulator.gr[r] += simulator.memory[effective_address]
        simulator._update_flags(simulator.gr[r])
        if simulator.debug:
            print(f"  EXECUTING: ADDA GR{r}, mem[{effective_address:04X}] -> GR{r} = {simulator.gr[r]}")
    else:
        print(f"Error: Memory read out of bounds at address {effective_address:04X}")
        simulator.is_running = False

def halt(simulator, r1, r2_or_x):
    """Halts the simulation."""
    print("\n--- Simulation Halted (HALT instruction) ---")
    simulator.is_running = False

def unknown(simulator, r1, r2_or_x):
    """Handles any unknown instructions."""
    # We need the original PC for the error message. It's `simulator.pr - 1`.
    start_pr = simulator.pr - 1 
    instruction_word = simulator.memory[start_pr]
    print(f"Error: Unknown instruction {instruction_word:04X} at address {start_pr:04X}")
    simulator.is_running = False

