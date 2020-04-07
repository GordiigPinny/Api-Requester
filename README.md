# Api-Requester
Submodule for all microservices

To add submodule to project:
```shell script
$ git submodule add https://github.com/GordiigPinny/ApiRequesters.git
```

For include this submodule you need package *dotenv*, *requests* and, of course, *django* and *django rest framework*:
```shell script
$ pip3 install dotenv
$ pip3 install requests
$ pip3 install django
$ pip3 install djangorestframework
```

Next, include next lines to the bottom of the *settings.py*:
```python
try:
    from ApiRequesters.settings import *
except ImportError as e:
    raise e
```