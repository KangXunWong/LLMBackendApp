from db import openaiclient, chatresponsecollection
from models import Conversation, ChatCompletion, KastomQuery, FilesResponse, Choices, Message, Usage
from settings import settings
from collections import ChainMap
from fastapi import HTTPException, UploadFile
from uuid import UUID
import uuid
from datetime import datetime
from log import log
import json
from pydantic import AnyUrl, AnyHttpUrl
import os
from werkzeug.utils import secure_filename
from typing import List, Optional

def convert_json_to_jsonl(filename):
    name, extension = filename.rsplit(".", 1).lower()
    with open(filename, 'r') as f:
        data = json.load(f)
    with open(f'{name}.jsonl', 'w') as f:
        for item in data:
            json.dump(item, f)
            f.write('\n')

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def flatten_dict(d):
    return dict(ChainMap(*[flatten_dict(v) if isinstance(v, dict) else {k: v} for k, v in d.items()]))

def object_to_dict(obj):
    """
    Recursively converts an object to a nested dictionary.

    Args:
        obj: The object to convert.

    Returns:
        dict: The nested dictionary representation of the object.
    """

    result = {}
    for attr, value in obj.__dict__.items():
        if isinstance(value, dict):
            result[attr] = object_to_dict(value)
        elif isinstance(value, list):
            result[attr] = [object_to_dict(item) for item in value]
        elif isinstance(value, str):
            result[attr] = value if value != 'None' else None
        else:
            try:
                result[attr] = object_to_dict(value)
            except (AttributeError, TypeError):
                result[attr] = repr(value) if repr(value) != 'None' else None
    return result

def create_conversation_crud(conversation: Conversation) -> dict:
    """"unpacks conversation query into one that openai accepts, and
    insert into mongodb the query +
    openai response (using empty message to force an ID and UUID) if successful"""
    messages=[{"role": "user", "content" : conversation.name}]
    try:
        response = openaiclient.chat.completions.create(model=settings.OPENAI_MODEL,messages=messages)
        if not response:
            log.info(f"Open AI chat creation failed")
            raise HTTPException(status_code=500, detail=f"Internal Server Error")
        response_dict = object_to_dict(response)
        log.info(response_dict)
        chat=ChatCompletion(user_queries=messages, **conversation.model_dump(), **response_dict)
        assert chat.uuid, HTTPException(status_code=500, detail="Internal Server Error: Conversation not created")
        document=chat.model_dump()
        result=chatresponsecollection.insert_one(document)
        log.info({"success":True, "message":"Conversation created", "Mongodb Object ID":chat.uuid})
        return {"id":chat.uuid}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

def retrieve_conversation_crud(user:str)-> list:
    """
    Manipulates the ChatCompletion model to return list of dictionary
    """
    results=chatresponsecollection.find({"user": user})
    list_of_convo=[]
    for doc in results:
        doc = ChatCompletion(**doc)
        dict_result={
            "id": doc.uuid,
            "name": doc.name,
            "params": doc.params,
            "tokens": doc.usage.total_tokens
        }
        list_of_convo.append(dict_result)
    log.info(list_of_convo)
    log.info({"success":True, "message":"Conversation retrieved", "Username":user})
    return list_of_convo

def update_conversation_crud(item_id:str, conversation: Conversation):
    """
    Update a conversation document, returns updateresult object
    """
    filter = {"uuid": UUID(item_id)}
    update = {"$set": conversation.model_dump()}
    result=chatresponsecollection.update_one(filter, update)
    log.info(result)
    log.info({"success":True, "message":"Conversation updated", "Mongodb Object ID":item_id})
    return result

def retrieve_conversation_history(item_id:str) -> ChatCompletion:
    """
    retrieve conversation based on item id
    """
    filter = {"uuid": UUID(item_id)}
    results=chatresponsecollection.find_one(filter)
    log.info(results)
    log.info({"success":True, "message":"Conversation history retrieved", "Mongodb Object ID":item_id})
    return ChatCompletion(**results) if results else None

def delete_conversation_crud(item_id:str) -> dict:
    filter = {"uuid": UUID(item_id)}
    results=chatresponsecollection.delete_one(filter)
    log.info(results)
    log.info({"success":True, "message":"Conversation deleted", "Mongodb Object ID":item_id})
    return results

def upload_file(file:UploadFile) -> FilesResponse:
    if not file:
        log.info({"success":False, "message":"No file part"})
    if file.filename == "":
        log.info({"success":False, "message":"No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex
        date_time = datetime.now().isoformat()
        new_filename = f"{unique_id}_{date_time}_{file.filename}"
        file_path = "./uploads" + new_filename
        try:
            with open(file_path, "wb") as f:
                for chunk in file.stream():
                    f.write(chunk)
            log.info({"success":True,"message":"File uploaded uploaded to server successfully","server_filename":new_filename})
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
        # Upload the file and add it to the Assistant (you could also add it to the message)
        uploaded_file = openaiclient.files.create(file=file.stream, purpose="assistants")
        # assistant_files = openaiclient.beta.assistants.files.list(assistant_id=assistant_id)
        # file_ids = [file.id for file in assistant_files.data]
        # file_ids.append(uploaded_file.id)
        # client.beta.assistants.update(
        #     assistant_id,
        #     file_ids=file_ids,
        # )
        log.info({"success":True,"message":"File uploaded to OpenAI successfully, adding to the query","uploaded_filename":filename})
    log.info({"success":False, "message":"File type not allowed"})
    return uploaded_file

def create_prompt_crud(prompt: KastomQuery, item_id:str, files: list[UploadFile]=None):
    """
    search for a conversation objection in conversation collection:
        1. if there is a created conversation available,
            a. reuse the conversation chat opened,
            b. append the query
            c. add in the openai response
        2. else return error
        3. if there are file data, add the file data into the prompt
    create a query to add into queries model
    """
    if files:
        file_uploaded=[upload_file(file) for file in files]
    keys=["role", "content"]
    log.info("hello world")
    history=retrieve_conversation_history(item_id)
    log.info(history)
    messagehistory=[]
    messagehistory.extend([queries.items() for queries in history.user_queries if queries.keys() in keys ])
    messagehistory.extend([choice.item() for choice in history.choices if choice.keys() in keys ])
    conversation_title= Conversation(**{k:v for k,v in history.items() if k in Conversation.model_fields.keys()})
    prompt=prompt.model_dump()
    messages=[{"role": "system", "content":"You are a credit rating report generator, generate for the user a structured format of credit report"}]+[{key:value for key, value in prompt.items() if key in keys}]+messagehistory
    try:
        response = openaiclient.chat.completions.create(model=settings.OPENAI_MODEL,messages=messages)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        chat=ChatCompletion(user_queries=messagehistory, **response, **conversation_title)
        document=chat.model_dump()
        result=chatresponsecollection.insert_one(document)
        return {"id":chat.uuid}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
