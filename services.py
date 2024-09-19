from db import openaiclient, chatresponsecollection
from models import Conversation, ChatCompletion, KastomQuery
from settings import settings
from collections import ChainMap
from fastapi import HTTPException


def flatten_dict(d):
    return dict(ChainMap(*[flatten_dict(v) if isinstance(v, dict) else {k: v} for k, v in d.items()]))

def create_conversation_crud(conversation: Conversation) -> dict:
    """"unpacks conversation query into one that openai accepts, and 
    insert into mongodb the query + 
    openai response (using empty message to force an ID and UUID) if successful"""
    # title=conversation.name
    # additional_properties=conversation.additionalProp1 if conversation.additionalProp1 is not None else None
    # params=flatten_dict(conversation.params) if conversation.params is not None else None
    messages=[]
    # for each in (title, additional_properties, params): 
    #     if isinstance(each, dict):
    #         messages.extend([{"role":"system", "content": value} for value in each.values()])
    #     else:
    #         messages.append({"role": "system", "content":each})
    try:
        response = openaiclient.chat.completions.create(model=settings.OPENAI_MODEL,messages=messages)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")        
        chat=ChatCompletion(query=conversation, **response)
        print(chat)
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
        doc = ChatCompletion(**doc)
        dict_result={
            "id": doc.uuid, 
            "name": doc.query.name, 
            "params": doc.query.params, 
            "additionalProp1":doc.query.additionalProp1,
            "tokens": doc.usage.total_tokens
        }
        list_of_convo.append(dict_result)
    return list_of_convo
    
def update_conversation_crud(item_id:str, conversation: Conversation):
    """
    Update a conversation document, returns updateresult object
    """
    filter = {"uuid": item_id}
    update = {"$set": conversation.model_dump()}
    result=chatresponsecollection.update_one(filter, update)
    return result

def retrieve_conversation_history(item_id:str) -> ChatCompletion:
    """
    retrieve conversation based on item id
    """
    filter = {"uuid": item_id}
    results=chatresponsecollection.find(filter)
    return ChatCompletion(results)

def delete_conversation_crud(item_id:str) -> dict:
    filter = {"uuid": item_id}
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
    filter = {"uuid": item_id}
    results=chatresponsecollection.find(filter)
    if result==0:
        return None 
    conversation_title= Conversation(**{k:v for k,v in results.items() if k in Conversation.model_fields.keys()})
    prompt=prompt.model_dump()
    keys=["role", "content"]
    messages=[{key:value for key, value in prompt.items() if key in keys}]
    try:
        response = openaiclient.chat.completions.create(model=settings.OPENAI_MODEL,messages=messages)
        chat=ChatCompletion(user_queries=prompt, **response, **conversation_title)
        document=chat.model_dump()
        result=chatresponsecollection.insert_one(document)
        return {"id":chat.uuid}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")