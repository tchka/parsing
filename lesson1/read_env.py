import os
from dotenv import load_dotenv

path = os.path.join(os.getcwd(), '.env')
print(path)
load_dotenv(path)

key = "USERNAME1"
value = os.getenv(key, None)
value1 = os.environ.get(key, None)

print(value)
print(value1)
