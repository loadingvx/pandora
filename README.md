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


##Segment fault helper
If your binary crashed online, and sadly, you knows nothing of disassamble, you will
need this python-script to help you get the function in which there is a 'BUG'.

* Now, segment-helper only get you the function, still not be able to explain why.
* Only Tested on (Linux 2.6.18-348.16.1.el5 x86_64 GNU/Linux)
* Hope this will be helpful.

```c
	//segmentfault.c
	#include <stdlib.h>
	
	void logic_function(void) {
	  char *ptr = 0x00;
	  *ptr = 'A';
	}
	
	int main(int argc, const char *argv[]) {
	  logic_function();
	  return EXIT_SUCCESS;
	}
```
While running, you will got a segment fault. try using segment-helper

```sh
	$ gcc segmentfault.c -o crash
	$ ./crash
	segmentation fault
	$ python %s ./crash

	Programme     : crash[29184]
	Operation     : user mode / write(0000000000000000) / NoPageFound
	Found Match   : [400458:    c6 00 41                movb   $0x41,(%%rax)]
	See Founction : <logic_function>

    $
```



