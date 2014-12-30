Pandora's ToolBox
=================

A toolbox for daily debuging and programming.

## [Util] Tabular
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
</pre>



## [Util] Segment fault helper
If your binary(release) crashed online, and sadly, you know nothing of disassamble,
this python-script will be helpful for you in that case.
Segment-fault helper will get you a function in which there is a 'BUG'.
* Segment-helper get you only the function where there is a segment fault.
* Tested Only on (Linux 2.6.18-348.16.1.el5 x86_64 GNU/Linux)

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

In practice, you will hit a segment fault with source code given above.
Try using segment-helper to tell which function contains the bug.

```sh
	$ gcc segmentfault.c -o crash
	$ ./crash
	segmentation fault
	$ python segment_fault_in_release.py ./crash
	
	Programme     : crash[29184]
	Operation     : user mode / write(0000000000000000) / NoPageFound
	Found Match   : [400458:    c6 00 41                movb   $0x41,(%%rax)]
	See Founction : <logic_function>
    $
```



