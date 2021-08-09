# Monkey Patching Reliably: PatchyMcPatchFace

## Description

Want to mock objects for unit testing? Want to automate application of your monkey patches? This is the package you are looking for

## Setup

> pip install patchymcpatchface

## How to use

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
    ```
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
    ```
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
