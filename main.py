

class Value:
   def __init__(self, val):
      self.value = [0] * 16
      
   def get(self):
      return self.value


LABELS = []
INSTRUCTIONS = []



# Execution Logic


GR = {
   "GR0" : 0,
   "GR1" : None,
   "GR2" : None,
   "GR3" : None,
   "GR4" : None,
   "GR5" : None,
   "GR6" : None,
   "GR7" : None,
}

FR = {
   "OF": 0,
   "SF": 0,
   "ZF": 0,
}

MEM = [None] * 65536

class Execution:
   def LD(r1, r2, x=0):
      if isGR(r2):
         GR[r1] = GR[r2]
      else:
         GR[r1] = MEM[r2+x]

   def ST(r1, adr, x=0):
      MEM[adr+x] = GR[r1]
   
   def LAD(r1, r2, x=0):
      GR[r1] = r2+x
   
   def AND(r1, r2, x=0):
      if isGR(r2):
         GR[r1] = GR[r1] & GR[r2]
      else:
         GR[r1] = GR[r1] & MEM[r2+x]

   def OR(r1, r2, x=0):
      if isGR(r2):
         GR[r1] = GR[r1] | GR[r2]
      else:
         GR[r1] = GR[r1] | MEM[r2+x]

   def XOR(r1, r2, x=0):
      if isGR(r2):
         GR[r1] = GR[r1] ^ GR[r2]
      else:
         GR[r1] = GR[r1] ^ MEM[r2+x] 

   def CPA(r1, r2, x=0):
      if isGR(r2):
         res = GR[r1] ^ GR[r2]
      else:
         res = GR[r1] ^ MEM[r2+x]
      flagRegist(res)       



def isGR(op):
   for i in range(1,8):
      if op == (f"GR{i}"):
         return True
   return False

def flagRegist(data):
   if data == 0:
      FR["ZF"] = 1
   else:
      FR["ZF"] = 0

   if data > 0:
      FR["SF"] = 0

# Compiler logic 


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