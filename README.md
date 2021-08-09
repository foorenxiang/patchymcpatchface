# Monkey Patching Reliably: PatchyMcPatchFace

## Description

Want to mock objects for unit testing? Want to automate application of your monkey patches? This is the package you are looking for

## Setup

> pip install patchymcpatchface
> import patchymcpatchface as pf

## How to use

There are 2 modes to use this package

1. Directly patch an object with pf.patch_apply
   - Useful for mocking in unit tests
2. For normal script execution, using patch hooks that automate patch application
   - Patch hook: Function defined in your patch modules that pf will automatically find and invoke on pf's import
   - Patch hooks also support delayed invocation if required

## Mocking for unit tests (Directly patching an object)

### Simple Usage Example

#### Install libraries

> pip install patchymcpatchface  
> pip install pytest (not required if not unit testing)

#### Your app file

- `main.py`

  ```python
  def hello_world():
      return "Hello World"


  def get_text():
      return hello_world()


  if __name__ == "__main__":
      print(get_text())
  ```

- run file
  > python3 main.py
  - result

    ```python
    Hello World
    ```

#### Your test file

- `test_main.py`

  ```python
  import patchymcpatchface as pf
  from main import get_text


  mock_hello_world = lambda *args, **kwargs: "hi world"


  def test_get_text():
      pf.patch_apply(
          "main.hello_world", mock_hello_world
      )

      result = get_text()
      assert result == "hi world"
  ```

- run test
  > pytest .
  - Test should pass because the `hello_world` function has been mocked with `hi world` return value.

### Real World Usage Example

#### Install libraries

> pip install patchymcpatchface pytest requests

#### Your app file

- `main.py`

  ```python
  from requests import request


  url = "https://jsonplaceholder.typicode.com/posts"
  body_request = {
      "title": "foo",
      "body": "bar",
      "userId": 1,
  }


  def http_request(method, url, request_body):
      response = request(method, url, json=request_body)
      return response


  if __name__ == "__main__":
      print(http_request("POST", url, body_request).json())
  ```

- run file
  > python3 main.py
  - result

    ```python
    {'title': 'foo', 'body': 'bar', 'userId': 1, 'id': 101}
    ```

#### Your test file

- `test_main.py`

  ```python
  import patchymcpatchface as pf
  from main import http_request

  url = "https://jsonplaceholder.typicode.com/posts"
  body_request = {
      "title": "foo",
      "body": "bar",
      "userId": 1,
  }


  def mock_request(*args, **kwargs):
      mock = type("mock_request", (), {})()
      mock.status_code = 201
      mock.json = lambda: {
          "title": "foo",
          "body": "bar",
          "userId": 1,
          "id": 123,
      }
      return mock


  def test_http_request():
      pf.patch_apply(
          "main.request", mock_request
      )

      response = http_request("POST", url, body_request)
      assert response.status_code == mock_request().status_code
      assert response.json() == mock_request().json()
  ```

- run test
  > pytest .
  - Test should pass because the `request` function from the `requests` library has been mocked with `{'title': 'foo', 'body': 'bar', 'userId': 1, 'id': 123}` return value.

## Automating patch application with patch hooks

### Simple Usage Example

#### Install library

> pip install patchymcpatchface

#### Your app file

- `main.py`

  ```python
  import patchymcpatchface as pf

  def hello_world():
      return "Hello World"
  
  def foo_bar():
      return "foo bar"


  if __name__ == "__main__":
      print(hello_world())
      print(foo_bar())
  ```

#### Your monkey patch files

- `hello_world_patch.py`

  ```python
  import patchymcpatchface as pf


  patched_hello_world = lambda *args, **kwargs: "hi world"


  def patch_hook():
      pf.patch_apply(
          "main.hello_world", patched_hello_world
      )
      print("Applied hello world patch")
  ```

`patch_hook` is a reserved function name to be placed at the module global level  
pf will look for this function and invoke it  

#### Your patch manifest file

- `patch_manifest.py` (placed at project root)

  ```python
  import hello_world_patch

  PATCH_MODULES = [
    hello_world_patch,
  ]
  ```

`patch_manifest.py` contains the list of patches that pf will apply

_Automatic patching on pf import_  
If `patch_manifest.py` is placed at project root with `PATCH_MODULES` defined, the patches will be automatically applied  
It can be be located elsewhere, but will not be automatically executed when pf is imported. See real world usage below for details

- run main
  > python3 main.py
  - result

    ```python
    Applied hello world patch
    hi world
    ```

### Real World Usage Example

#### Your monkey patch files

- `hello_world_patch.py`

  ```python
  import patchymcpatchface as pf


  patched_hello_world = lambda *args, **kwargs: "hi world"


  def patch_hook():
      pf.patch_apply(
          "main.hello_world", patched_hello_world
      )
      print("Applied hello world patch")
  ```

- `foo_bar_patch.py`

  ```python
  import patchymcpatchface as pf


  patched_foo_bar = lambda *args, **kwargs: "bar foo"


  def patch_hook():
      pf.patch_apply(
          "main.foo_bar", patched_foo_bar
      )
      print("Applied foo bar patch")
  ```

`patch_hook` is a reserved function name to be placed at the module global level  
pf will look for this function and invoke it  
#### Your patch manifest file

- `patch_manifest.py` (placed in hello_package)

  ```python
  import hello_world_patch
  from typing import List
  from types import ModuleType

  PATCH_MODULES: List[ModuleType] = [
    hello_world_patch,
    # you can list other modules containing monkey patches and patch_hook here
  ]
  ```

- `patch_manifest.py` (placed in foo_package)

  ```python
  import foo_bar_patch
  from typing import List
  from types import ModuleType

  PATCH_MODULES: List[ModuleType] = [
    foo_bar_patch,
    # you can list other modules containing monkey patches and patch_hook here
  ]
  ```

`patch_manifest.py` contains the list of patches that pf will apply

_Automatic patching on pf import_  
If a `patch_manifest.py` is placed at project root with `PATCH_MODULES` defined, the patches will be automatically applied  

_Other means of invoking automatic patching_  
If `patch_manifest.py` is:

- In a different location  
and/or  
- Multiple patch manifests are desired  
and/or  
- Delayed invocation is desired for specific patches  
Use `pf.invoke_patch_hooks` to register and invoke the patches. See below for example:

#### Your app file

- `main.py`

  ```python
  import patchymcpatchface as pf
  from hello_package.patch_manifest_hello import PATCH_MODULES_HELLO
  from foo_package.patch_manifest_foo import PATCH_MODULES as PATCH_MODULES_FOO

  def hello_world():
      return "Hello World"
  
  def foo_bar():
      return "foo bar"


  if __name__ == "__main__":
      # apply patches at start of program
      pf.invoke_patch_hooks(PATCH_MODULES_HELLO)
      
      # run the patched function registered by PATCH_MODULES
      print(hello_world())
      
      # call the original function
      print(foo_bar()) 
      
      # delayed patch invocation for foo_bar
      pf.invoke_patch_hooks(PATCH_MODULES_FOO)
      
      # run the patched function registered by PATCH_MODULES_FOO
      print(foo_bar())
  ```

- run main
  > python3 main.py
  - result

    ```python
    Applied hello world patch
    hi world
    foo bar
    Applied foo bar patch
    bar foo
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

After importing package_to_be_patched.foo ___module___ in the patch module, the imported module will be loaded and bounded to the global namespace with the following keys. Yes, multiple keys for a single ___module___ import!

Afterwards, the patch is robust against how the other modules import this function!

```python
filter_sys_modules("package_to_be_patched"): {'package_to_be_patched': <module 'package_to_be_patched' (namespace)>,
                                      'package_to_be_patched.foo': <module 'package_to_be_patched.foo' from '/Users/foorx/Developer/python_patching_experiment/package_to_be_patched/foo.py'>}
```

Testing various methods of importing the target function to be patched in module foo yields a consistent result:

```text
__main__
Running target_function_direct()
I'm the patched function

__main__
Running package_to_be_patched.foo.target_function()
I'm the patched function

running_package.foo
from package_to_be_patched.foo import target_function
Running target_function()
I'm the patched function

running_package.bar
import package_to_be_patched
Running package_to_be_patched.foo.target_function()
I'm the patched function

running_package.baz
import package_to_be_patched.foo
Running package_to_be_patched.foo.target_function()
I'm the patched function


running_package.foobar
from package_to_be_patched.foo import *
Running target_function()
I'm the patched function

running_package.bazbar
import package_to_be_patched.foo
Running package_to_be_patched.foo.target_function()
I'm the other patched function
```
