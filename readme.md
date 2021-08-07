# Monkey Patching Reliably: PatchyMcPatchFace

## Description

## Setup

> pip3 install patchymcpatchface

## How to use

### Simple Usage Example

#### Install libaries

> pip3 install patchymcpatchface pytest

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
  - Test should pass as the return value of `hello_world` has been mocked

### Real World Usage Example

#### Install libaries

> pip3 install patchymcpatchface pytest requests

#### Your app file

- `main.py`

  ```python
  from requests import request


  URL = "https://jsonplaceholder.typicode.com/posts"
  body_request = {
      "title": "foo",
      "body": "bar",
      "userId": 1,
  }


  def http_request(method, url, request_body):
      response = request(method, URL, json=request_body)
      return response


  if __name__ == "__main__":
      print(http_request("POST", URL, body_request).json())
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

  URL = "https://jsonplaceholder.typicode.com/posts"
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


  def test_requests():
      pf.patch_apply(
          "deco.request", mock_request
      )

      response = http_request("POST", URL, body_request)
      assert response.status_code == mock_request().status_code
      assert response.json() == mock_request().json()
  ```

- run test
  > pytest .
  - Test should pass as the return value of `{'title': 'foo', 'body': 'bar', 'userId': 1, 'id': 123}` has been mocked
