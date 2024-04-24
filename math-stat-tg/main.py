from tkinter.filedialog import askopenfilename

from cusum import *
from imrx import *
from emwa import *
from xbar_rbar import *
from xbar_sbar import *
from memwa import *

# TODO - function to choose the type of chart3
# TODO - names of charts

path_file = askopenfilename()

# print("1. emwa (len subgroup = 1) \n2. memwa\n3. xbar_rbar (len subgroup 2 to 8)\n4. xbar_sbar (len subgroup from 9)\n5. imrx (len subgroup = 1)\n6. cusum (len subgroup = 1)")

t = memwa()
t.gen(path_file)

print(t.allData())
print(t.memwaPoints())
print(t.memwaLimitUp())
print(t.memwaLimitDown())