# Table2Dict

Table2Dict converts an html table (1D or 2D) in a list, a dictionnary or get useful informations about table. It accepts as parameter either absolute path to an `.html` file (with only one table inside) or directly table's beautiful soup tag `<bs4.element.Tag>`.

It can also return the full table converted to a JSON object or return only the table header, body or the full table converted 
to a raw list.

## Usage

```python
import Table2Dict
```

Convert an `.html` file with one table inside to an ordered or a standard dictionnary :

```python
# Absolute path of .html file
tableAbsolutePath = "/Users/Kim/Project/myTables/myTable1.html"

# Create Table object
tableObj = Table2Dict.Table(tableAbsolutePath)

# Get ordered dict (to keep original order of columns)
myOrdDict = tableObj.getTableDict(dictType="ordered")

# Get dict (default)
myDict = tableObj.getTableDict()
```
