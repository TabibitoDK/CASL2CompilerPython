
# 'h' stands for signed 16-bit integer
MEM = [None] * 65536
print(MEM)
print(MEM[0])  # Accessing elements


LABELS = []
INSTRUCTIONS = []


class Label:
   def __init__(self, label, value, type):
      self.label = label
      self.value = value
      self.type = type

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
        lb = Label(self.label, self.address, labelType(self.instruction))
        LABELS.append(lb)

def firstPass(txt):
   strings = txt.split("\n")
   for s in strings:
      cmd = s.split(" ")
      if cmd[0] == '':
         cmd[0] = None
      Instruction(cmd[0], cmd[1], cmd[2])
   

def secondPass(INSTRUCTIONS):
   for instruction in INSTRUCTIONS:
      for op in instruction.operands:
         if findLabel(op) != -1:
            op = findLabel(op)

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


def findLabel(label):
   loc = 0
   for lb in LABELS:
      if lb == label:
         return loc
      loc += 1
   return -1


def labelType(instruction):
   if instruction == "DC":
      return 0
   elif instruction == "DS":
      return 1