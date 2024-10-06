import pymongo
from settings import settings
from openai import OpenAI, APIConnectionError
from bson.binary import UuidRepresentation
from log import log

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
            log.info("Connected to MongoDB successfully!")
        else:
            log.info("Failed to connect to MongoDB.")
    except pymongo.errors.ServerSelectionError as err:
        log.info(f"Error connecting to MongoDB: {err}")
    # try:
    #     if not openaiclient:
    #         raise ValueError("Missing OPENAI_API_KEY environment variable")
    #     response = openaiclient.chat.completions.create(
    #     model=settings.OPENAI_MODEL,messages=[
    #     {
    #         "role": "user",
    #         "content": "Say this is a test",
    #     }
    # ]
    #     )
    #     log.info(response.model_dump())
    # except APIConnectionError as err:
    #     log.info("The server could not be reached")
    #     log.info(err.__cause__)
