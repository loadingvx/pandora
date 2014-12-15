Pandora's ToolBox
=================

A toolbox for daily debuging and programming.

##Tabular
A ascii table render.
* Use function 'row' to add one row to table
* Call 'render' to show final table

Usage:

```python
	import tabular
	t = tabular.Tabular()
	t.row({'id':3, 'name':'Michael Jackson',  'age':'28'})
	t.row({'id':2, 'name':'Pandora Avatar', 'age':'28'})
	t.row({'id':1, 'name':'Jack Jones', 'age':'28'})
	t.row({'id':1, 'name':'路人甲', 'age':'28'})
	t.render('id')
```

output:
<pre>
	+---+----+-----------------+
	| id| age| name            |
	+---+----+-----------------+
	| 3 | 28 | Michael Jackson |
	| 2 | 28 | Pandora Avatar  |
	| 1 | 28 | Jack Jones      |
	| 1 | 28 | 路人甲           |
	+---+----+-----------------+
<pre>



