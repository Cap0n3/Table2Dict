'''
File to do random testing about anything that's needed.
'''
import os
from bs4 import BeautifulSoup
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from BandAPI.CustomPackage.ExtractTableMod import ExtractTable

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
tableObj = ExtractTable(absPath)
print(tableObj.getTableDict())
