# Table2Dict

Module to convert an html table (1D or 2D) in a list or a dictionnary or to obtain usful informations about given table. 

It accepts as parameters either absolute path to an `.html` file (with only one table inside) or directly table's beautiful soup tag `<bs4.element.Tag>`.

It can also return the full table converted to a JSON object or return only the table header, body or the full table converted 
to a raw list.

## Usage

Convert an `.html` file with one table inside to an ordered or a standard dictionnary :

```python
tableAbsolutePath = "/Users/Kim/Project/myTables/myTable1.html"
# Create object
tableObj = Table2Dict(tableAbsolutePath)

# Get ordered dict (to keep original order of columns)
myOrdDict = tableObj.getTableDict(dictType="ordered")

# Get dict (default)
myDict = tableObj.getTableDict()
```