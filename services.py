from db import openaiclient, chatresponsecollection
from models import Conversation, ChatCompletion, KastomQuery
from settings import settings
from collections import ChainMap
from fastapi import HTTPException
from uuid import UUID
from log import logging

def flatten_dict(d):
    return dict(ChainMap(*[flatten_dict(v) if isinstance(v, dict) else {k: v} for k, v in d.items()]))

def create_conversation_crud(conversation: Conversation) -> dict:
    """"unpacks conversation query into one that openai accepts, and 
    insert into mongodb the query + 
    openai response (using empty message to force an ID and UUID) if successful"""
    messages=[]
    try:
        response = openaiclient.chat.completions.create(model=settings.OPENAI_MODEL,messages=messages)
        if response.status_code != 200:
            logging.info(f"API request failed with status code {response.status_code}")  
            raise HTTPException(status_code=500, detail=f"Internal Server Error")      
        chat=ChatCompletion(query=conversation, **response)
        logging.info(chat)
        document=chat.model_dump()
        result=chatresponsecollection.insert_one(document)
        return {"id":chat.uuid}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
            
def retrieve_conversation_crud()-> list:
    """
    Manipulates the ChatCompletion model to return list of dictionary
    """
    results=chatresponsecollection.find()
    list_of_convo=[]
    for doc in results: 
        logging.info(doc)
        doc = ChatCompletion(**doc)
        dict_result={
            "id": doc.uuid, 
            "name": doc.name, 
            "params": doc.params, 
            "additionalProp1":doc.additionalProp1,
            "tokens": doc.usage.total_tokens
        }
        list_of_convo.append(dict_result)
    logging.info(list_of_convo)
    return list_of_convo
    
def update_conversation_crud(item_id:str, conversation: Conversation):
    """
    Update a conversation document, returns updateresult object
    """
    filter = {"uuid": UUID(item_id)}
    update = {"$set": conversation.model_dump()}
    result=chatresponsecollection.update_one(filter, update)
    return result

def retrieve_conversation_history(item_id:str) -> ChatCompletion:
    """
    retrieve conversation based on item id
    """
    filter = {"uuid": UUID(item_id)}
    results=chatresponsecollection.find_one(filter)
    return ChatCompletion(**results) if results else None

def delete_conversation_crud(item_id:str) -> dict:
    filter = {"uuid": UUID(item_id)}
    results=chatresponsecollection.delete_one(filter)
    return results

def create_prompt_crud(prompt: KastomQuery, item_id:str):
    """
    search for a conversation objection in conversation collection: 
        1. if there is a created conversation available, 
            a. reuse the conversation chat opened, 
            b. append the query
            c. add in the openai response
        2. else return error
    create a query to add into queries model
    """
    filter = {"uuid": UUID(item_id)}
    results=chatresponsecollection.find_one(filter)
    if result==0:
        return None 
    conversation_title= Conversation(**{k:v for k,v in results.items() if k in Conversation.model_fields.keys()})
    prompt=prompt.model_dump()
    keys=["role", "content"]
    messages=[{key:value for key, value in prompt.items() if key in keys}]
    try:
        response = openaiclient.chat.completions.create(model=settings.OPENAI_MODEL,messages=messages)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")       
        chat=ChatCompletion(user_queries=prompt, **response, **conversation_title)
        document=chat.model_dump()
        result=chatresponsecollection.insert_one(document)
        return {"id":chat.uuid}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")