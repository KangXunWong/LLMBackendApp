import pymongo
from settings import settings
from openai import OpenAI

# monogdb access
pymongoclient = pymongo.MongoClient(settings.DB_URL)
db = pymongoclient[settings.DB_NAME]
# Access a chatresponsecollection within the database
chatresponsecollection = db['conversations']

# openapi access
openaiclient = OpenAI(api_key=settings.OPENAI_API_KEY)

if __name__ == "__main__": 
    try: 
        if pymongoclient.server_info():
            print("Connected to MongoDB successfully!")
        else:
            print("Failed to connect to MongoDB.")
    except pymongo.errors.ServerSelectionError as err:
        print(f"Error connecting to MongoDB: {err}")
    try:
        if not openaiclient: 
            raise ValueError("Missing OPENAI_API_KEY environment variable")
        response = OpenAI.Completion.create(
            engine="text-davinci-003",
            prompt="Hello, world!",
            max_tokens=10
        )
        print(response.choices[0].text)
    except OpenAI.APIConnectionError as err: #to fix 
        print(f"Error connecting to OpenAI: {err}")
