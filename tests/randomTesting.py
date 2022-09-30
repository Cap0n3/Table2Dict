'''
File to do one-the-go testing about anything that's needed.
'''
import os
from bs4 import BeautifulSoup
import inspect
import sys

# Go to parent folder to find module
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.Table2Dict_Cap0n3 import Table2Dict

# For Windows (relative path) 
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Test_Wiki_Table/Test_Tables/debugTable_case0.html')

# Open html file
with open(filename, 'r') as htmlTestFile:
    soup = BeautifulSoup(htmlTestFile, "html.parser")

# Get table tag in soup (Test 1)
tableSoup = soup.find('table')

# Absolute path (Test 2)
absPath = filename

# ========= TESTING ========= #
tableObj = Table2Dict.Table(absPath)
print(tableObj.getTableDict())
