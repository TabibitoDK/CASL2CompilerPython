
# 'h' stands for signed 16-bit integer
MEM = [None] * 65536
print(MEM)
print(MEM[0])  # Accessing elements


LABELS = []
INSTRUCTIONS = []


class Label:
   def __init__(self, label, value):
      self.label = label
      self.value = value

class Instruction:
  def __init__(self, label, instruction, operands):
    self.label = label
    self.instruction = instruction
    self.operands = operands
    INSTRUCTIONS.append(self)
    self.address = len(INSTRUCTIONS)-1
    if self.label != None:
       self.saveLABEL(self)

  def saveLABEL(self):
    if isNewLABEL(self.label):
        lb = Label(self.label, self.address)
        LABELS.append(lb)

def firstPass(txt):
   strings = txt.split("\n")
   for s in strings:
      cmd = s.split(" ")
      if cmd[0] == '':
         cmd[0] = None
      Instruction(cmd[0], cmd[1], cmd[2])
   
   

def isNewLABEL(label):
    for lb in LABELS:
      if lb == label:
         return False
    return True

def isDC(instruction):
   if instruction == "DC":
      return True
   else:
      return False

def isDS(instruction):
   if instruction == "DS":
      return True
   else:
      return False