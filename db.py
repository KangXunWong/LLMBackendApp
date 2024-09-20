import pymongo
from settings import settings
from openai import OpenAI
from bson.binary import UuidRepresentation
from log import logging

# monogdb access
pymongoclient = pymongo.MongoClient(settings.DB_URL, uuidRepresentation='standard')
db = pymongoclient[settings.DB_NAME]
# Access a chatresponsecollection within the database
chatresponsecollection = db['conversations']

# openapi access
openaiclient = OpenAI(api_key=settings.OPENAI_API_KEY)

if __name__ == "__main__": 
    try: 
        if pymongoclient.server_info():
            logging.info("Connected to MongoDB successfully!")
        else:
            logging.info("Failed to connect to MongoDB.")
    except pymongo.errors.ServerSelectionError as err:
        logging.info(f"Error connecting to MongoDB: {err}")
    try:
        if not openaiclient: 
            raise ValueError("Missing OPENAI_API_KEY environment variable")
        response = openaiclient.chat.completions.create(
        model=settings.OPENAI_MODEL,messages="Hello world"
        )
        logging.info(response.choices[0].text)
    except Exception as err: 
        logging.info(f"Error connecting to OpenAI: {err}")
