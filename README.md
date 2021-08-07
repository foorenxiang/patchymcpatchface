# Monkey Patching Reliably: PatchyMcPatchFace

## A monkey patching library that uses only Python standard library

### `pip install patchymcpatchface`

## How to use this?

### `import patchymcpatchface as pf`

### There are 2 ways this package can be used:

1. Mock objects in unit testing
2. Automatically apply monkey patches in patch modules through hooks

## Mock objects in unit testing

- Call pf.apply_patch("object.to.patch":str, patch_object: Any) prior to importing your module to be patched

```python
import patchymcpatchface as pf


def test_requests():
    patch_class_method = lambda *args, **kwargs: "I am the patched lambda"

    pf.patch_apply(
        "package_to_be_patched.request_call.Session.request",
        patch_class_method
    )
    from package_to_be_patched.request_call import requests_function

    patched_result =  requests_function()
```

## Automatically apply monkey patches in patch modules through hooks

- import patchymcpatchface as pf
  - This automatically applies patches listed in patch_manifest.py on your project root (See below for details)

  - pf.invoke_patch_hooks(YOUR_CUSTOM_PATCH_HOOKS_LIST) for delayed patch invocation

### What patch configuration files you need to create in your project

1. `patch_manifest.py (optional file on project root)`
2. `any_other_patch_manifests_of_any_name_you_create.py (placed anywhere in your project)`

How a patch module will look like:

```python
def patch_function():
    printout = "I'm the patched function\n"
    print(printout)
    return printout

patch_object = {"foo": "bar"}

patch_object_method = lambda *args, **kwargs: "something"

# define this patch_hook (reserved function name) for patchymcpatchface to pick up
from patchymcpatchface import patch_apply
def patch_hook():  
    # put in the full module ancestry and the patch function as parameters
    # note that you should include the package, module and object ancestry as a string
    patch_apply(
        "patching_example.mypackage.foo.target_function", patch_function 
    )  
    patch_apply(
        "patching_example.mypackage.foo.target_object", patch_object
    )  
    patch_apply(
        "patching_example.mypackage.foo.target_class.target_method", patch_object_method
    )  
```

Define patch modules in patch_manifest.py on project root and/or similar patch manifest modules placed elsewhere in your source  
The patch modules listed in patch_manifest.py on project root will be patched automatically when you import patchymcpatchface
To have patches invoke in a delayed manner, or if you would like the patches manifest to be placed else in your project, create other manifest module(s) at any location in your source, that contains a manifest variable of type List[ModuleType] as an export  
See the next section below to see how this custom manifest variable should be applied  

```python
# import your patch modules here and document them in PATCH_MODULES below
import patching_example.patch_package.baz as baz
import patching_example.patch_package.foobaz as foobaz
from typing import List
from types import ModuleType

# update this list with modules that contain patch_hook
PATCH_MODULES: List[ModuleType] = [
    baz,
]
```

How to apply patches automatically:

```python
# import patchymcpatchface before imports of other modules that should be patched 
# it automatically invokes all patch hooks when imported
import patchymcpatchface as pf

pf
```

To delay invocation of certain patches, you may define other patch manifest modules that has an exportable List[ModuleType] variable containing patch modules with the patch_hook defined.  
Then, in the point of your code where you would like the patches to be invoked:

```python
import patchymcpatchface as pf 
from where.you.placed.your.custom.manifest.module import YOUR_CUSTOM_PATCH_HOOKS_LIST

...
...
...
# code you are running before you want to invoke the patch
pf.invoke_patch_hooks(YOUR_CUSTOM_PATCH_HOOKS_LIST)
#code you are running before you want to invoke the patch
...
...
...
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

After importing patching_example.mypackage.foo ___module___ in the patch module, the imported module will be loaded and bounded to the global namespace with the following keys. Yes, multiple keys for a single ___module___ import!

Afterwards, the patch is robust against how the other modules import this function!

```python
filter_sys_modules("patching_example.mypackage"): {'patching_example.mypackage': <module 'patching_example.mypackage' (namespace)>,
                                      'patching_example.mypackage.foo': <module 'patching_example.mypackage.foo' from '/Users/foorx/Developer/python_patching_experiment/patching_example.mypackage/foo.py'>}
```

Testing various methods of importing the target function to be patched in module foo yields a consistent result:

```text
__main__
Running target_function_direct()
I'm the patched function

__main__
Running patching_example.mypackage.foo.target_function()
I'm the patched function

patching_example.running_package.foo
from patching_example.mypackage.foo import target_function
Running target_function()
I'm the patched function

patching_example.running_package.bar
import patching_example.mypackage
Running patching_example.mypackage.foo.target_function()
I'm the patched function

patching_example.running_package.baz
import patching_example.mypackage.foo
Running patching_example.mypackage.foo.target_function()
I'm the patched function


patching_example.running_package.foobar
from patching_example.mypackage.foo import *
Running target_function()
I'm the patched function

patching_example.running_package.bazbar
import patching_example.mypackage.foo
Running patching_example.mypackage.foo.target_function()
I'm the other patched function
```
