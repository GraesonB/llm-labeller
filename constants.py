from dotenv import load_dotenv
import os
load_dotenv()

HELLO_ENV = os.getenv('HELLO_ENV')
print(HELLO_ENV)
