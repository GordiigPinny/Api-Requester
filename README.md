# Api-Requester
Submodule for all microservices

For include this submodule you need package dotenv and requests:
```shell script
$ pip3 install dotenv
$ pip3 install requests
```

Next, include next lines to the bottom of the *settings.py*:
```python
try:
    from ApiRequester.settings import *
except ImportError as e:
    raise e
```