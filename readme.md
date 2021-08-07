# Monkey Patching reliably

## Monkey Patching strategy requiring only standard Python library

### What functional files you need to copy into your project

1. `patch_apply.py`
2. `patcher.py`
3. `patch_manifest.py (optional file on project root`
4. `any_other_patch_manifests_of_any_name_you_create.py (placed anywhere in your project)`

How a patch module will look like:

```python
def patch_function():
    printout = "I'm the patched function\n"
    print(printout)
    return printout

# define this patch_hook (reserved function name) for patcher to pick up
def patch_hook():  
    from patch_apply import patch_apply

    # put in the full module ancestry and the patch function as parameters
    # note that you should include the package, module and object ancestry as a string
    patch_apply(
        "mypackage.foo.target_function", patch_function 
    )  
```

Define patch modules in patch_manifest.py on project root and/or similar patch manifest modules placed elsewhere in your source  
The patch modules listed in patch_manifest.py on project root will be patched automatically when you import patcher  
To have patches invoke in a delayed manner, or if you would like the patches manifest to be placed else in your project, create other manifest module(s) at any location in your source, that contains a manifest variable of type List[ModuleType] as an export  
See the next section below to see how this custom manifest variable should be applied  

```python
# import your patch modules here and document them in PATCH_MODULES below
import patch_package.baz as baz
import patch_package.foobaz as foobaz
from typing import List
from types import ModuleType

# update this list with modules that contain patch_hook
PATCH_MODULES: List[ModuleType] = [
    baz,
]
```

To delay invocation of certain patches, you may define other patch manifest modules that has an exportable List[ModuleType] variable containing patch modules with the patch_hook defined.  
Then, in the point of your code where you would like the patches to be invoked:

```python
from patcher import invoke_patch_hooks
from where.you.placed.your.custom.manifest.module import YOUR_CUSTOM_PATCH_HOOKS_LIST

...
...
...
# code you are running before you want to invoke the patch
invoke_patch_hooks(YOUR_CUSTOM_PATCH_HOOKS_LIST)
#code you are running before you want to invoke the patch
...
...
...
```

How to apply patches:

```python
# import patcher before imports of other modules that should be patched 
# it automatically invokes all patch hooks when imported
import patcher

patcher
```

## How this works

<https://realpython.com/python-import/#import-internals>

To quote real python:

```text
The details of the Python import system are described in the official documentation. At a high level, three things happen when you import a module (or package). The module is:  

- Searched for
- Loaded
- Bound to a namespace

For the usual imports—those done with the import statement—all three steps happen automatically. When you use importlib, however, only the first two steps are automatic. You need to bind the module to a variable or namespace yourself.  
```

After importing mypackage.foo ___module___ in the patch module, the imported module will be loaded and bounded to the global namespace with the following keys. Yes, multiple keys for a single ___module___ import!

Afterwards, the patch is robust against how the other modules import this function!

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
from mypackage.foo import target_function
Running target_function()
I'm the patched function

running_package.bar
import mypackage
Running mypackage.foo.target_function()
I'm the patched function

running_package.baz
import mypackage.foo
Running mypackage.foo.target_function()
I'm the patched function


running_package.foobar
from mypackage.foo import *
Running target_function()
I'm the patched function

running_package.bazbar
import mypackage.foo
Running mypackage.foo.target_function()
I'm the other patched function
```
