import sys
import dotenv

TESTING = sys.argv[1:2] == ['test']

__DEV_ENV_FILE_NAME = 'debug.env'
__PROD_ENV_FILE_NAME = 'prod.env'

ENV_FILE_NAME = __PROD_ENV_FILE_NAME if DEBUG else __DEV_ENV_FILE_NAME

ENV = dotenv.main.dotenv_values(ENV_FILE_NAME)

ALLOW_REQUESTS = not DEBUG
