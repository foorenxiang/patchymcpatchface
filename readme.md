# How this works

https://realpython.com/python-import/#import-internals

To quote real python:

```
The details of the Python import system are described in the official documentation. At a high level, three things happen when you import a module (or package). The module is:  

- Searched for
- Loaded
- Bound to a namespace

For the usual imports—those done with the import statement—all three steps happen automatically. When you use importlib, however, only the first two steps are automatic. You need to bind the module to a variable or namespace yourself.  
```

After importing mypackage.foo ___module___ in the patch module, the imported module will be loaded and bounded to the global namespace with the following keys. Yes, multiple keys for a single ___module___ import!

```python
filter_sys_modules("mypackage"): {'mypackage': <module 'mypackage' (namespace)>,
                                      'mypackage.foo': <module 'mypackage.foo' from '/Users/foorx/Developer/python_patching_experiment/mypackage/foo.py'>}
```

Testing various methods of importing the target function to be patched in module foo yields a consistent result:

```text
__main__
Running target_function_direct()
I'm the patched function

__main__
Running mypackage.foo.target_function()
I'm the patched function

running_package.foo
Running target_function()
I'm the patched function

running_package.bar
Running mypackage.foo.target_function()
I'm the patched function

running_package.baz
Running mypackage.foo.target_function()
I'm the patched function
```

Summary:
Exactly import the module to be patched (not the package, nor the actual function to be patched)
Assign in sys.modules the parent package key if applicable, and directly overwrite the function to be patched, as the package/module attribute

```python
import sys
import mypackage.foo
from patch_package.baz import patch_function

mypackage


def patch():
    sys.modules["mypackage"].foo.target_function = patch_function
    # you can list all other functions to be patched here
```
