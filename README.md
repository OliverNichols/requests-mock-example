
# requests_mock

## Overview

The `requests_mock` module is used to mock the responses obtained from the `requests` module.  
We can use the `requests_mock` module in our unit tests when the app being tested makes use of the `requests` module.

## Why do we use it?

We need to mock requests if we don't expect the `requests` to function correctly in our test cases.  
For example, we may expect them to fail if they rely on other containers. 

Since we are mocking the application in our test cases, it is important to remember that our containers are never created or understood by `pytest`, and so this is neccessary.

The point of testing in this way is to make sure the data gathered from our requests is used or displayed correctly, and we should still create tests to check any other services work correctly too.

## Syntax

In order to mock our requests, we must import `requests_mock` and we will be using `requests_mock.mock` as our mocker. You may also choose to use `requests_mock.Mocker`.

The syntax for using this mocker to manage the context of a request is as follows:

```py
with requests_mock.mock() as m:
    m.<method>('<url>', <attribute>=<value>)

    # now we can do whatever we want with the corresponding request and 
    # it's <attribute> will always be <value>

    # make sure it's indented!!
```

Such as

### GET
- `m.get('<url>', text='<>')` -> `requests.get('<url>').text` 
- `m.get('<url>', json=<>)` -> `requests.get('<url>').json()`

### POST
- `m.post('<url>', text='<>')` -> `requests.post('<url>', data=<>, json=<>).text`
- `m.post('<url>', json='<>')` -> `requests.post('<url>', data=<>, json=<>).json()`


## Example

Let's say our application looks something like the following:

```py
import requests

@app.route('/')
def index():
    food = requests.get('http://service-2:5000/get/food').text
    drink = requests.get('http://service-3:5000/get/drink').text

    payload = {'food': food, 'drink': drink}
    price = requests.post('http://service-4:5000/post/order', json=payload).json()

    return f"You ordered a {food} and a {drink} for £{price}.\n"
```

We can mock our requests in the following way:

```py
import requests_mock

class TestResponse(TestBase):

    def test_index(self):

        with requests_mock.mock() as m:
            m.get('http://service-2:5000/get/food', text='Margherita')
            m.get('http://service-3:5000/get/drink', text='Stella Artois')
            m.post('http://service-4:5000/post/order', json=16.78)

            response = self.client.get(url_for('index'))

        self.assert200(response)
        self.assertIn('You ordered a Margherita and a Stella Artois for £16.78.', response.data.decode())
```

## Tutorial

### Creating the directory structure

From your home directory, run the commands:

```bash
mkdir example-requests-mock && cd $_
mkdir tests
touch app.py tests/test_unit.py
```

### Installing dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip3 install flask flask_testing requests requests_mock pytest
```

### Creating the example app

Configure your `app.py` as follows:

`app.py`:
```py
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    example_text = requests.get('http://backend:5000/get/text').text # doesn't exist
    return f'{example_text}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

If we spin up this application using `python3 app.py`, and run `curl localhost:5000` in another terminal, we should just get a 500 error.

### Creating the the test case

Configure your `tests/test_unit.py` as follows:

`tests/test_unit.py`:
```py
from flask_testing import TestCase
import requests_mock
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestResponse(TestBase):
    def test_index(self):
        with requests_mock.mock() as m:
            m.get('http://backend:5000/get/text', text='Some text, idk.')
            
            response = self.client.get('/')
            self.assertIn(b'Some text, idk.', response.data)
```

Notice how we assert that the response's text should now look like the text we included in our mocked request.

### Run the tests

Now we are ready to run the tests - use `python3 -m pytest`.

## Exercises

There are no exercises for this module.