from fastapi import FastAPI, Path, Query, HTTPException
from models import Conversation, KastomQuery
from services import create_conversation_crud, retrieve_conversation_crud, update_conversation_crud, retrieve_conversation_history, delete_conversation_crud,create_prompt_crud
from log import log_function, logging

app = FastAPI()

@log_function
@app.post("/conversations", status_code=201, summary = 'Creates a new Conversation with an LLM model', description = 'A Conversation describes a series of interactions with an LLM model. It also contains the properties that will be used to send individual queries to the LLM. Chat queries will be anonymised and logged for audit purposes')
async def create_conversation(conversation: Conversation):
    try: 
        return create_conversation_crud(conversation)
    except ValueError as e:
        logging.info("An value error occurred:", e)
        raise HTTPException(status_code=400, detail="Invalid parameters provided")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

@log_function
@app.get("/conversations", status_code=200,summary="Retrieve a user's Conversation", description="Retrieves all the conversations that a user has created, the conversation history is not provided here.")
async def retrieve_conversation():
    try: 
        return retrieve_conversation_crud()
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

@log_function
@app.put("/conversations/{item_id}", status_code=204, summary="Updates the LLM properties of a Conversations", description="Allows the user to customise parameters and properties of a Conversation, thereby customising their experience")
async def update_conversation(conversation:Conversation, item_id: str = Path(..., title="A unique ID string")):
    try:
        result = update_conversation_crud(item_id, conversation)
        logging.info(result)
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Specified resource(s) was not found")
    except ValueError as e:
        logging.info("An value error occurred:", e)
        raise HTTPException(status_code=400, detail="Invalid parameters provided")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

@log_function
@app.get("/conversations/{item_id}", status_code=200, summary="Retrieves the Conversation History", description="Retrieves the entire conversation history with the LLM")
async def retrieve_history(item_id: str = Path(..., title="A unique ID string")):
    try: 
        result = retrieve_conversation_history(item_id)
        if result:
            return result
        else:
            logging.info(f"Unable to find resource: {item_id}" )
            raise HTTPException(status_code=404, detail="Specified resource(s) was not found")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

@log_function
@app.delete("/conversations/{item_id}", status_code=204, summary="Deletes the Conversation", description="Deletes the entire conversation history with the LLM Model")
async def delete_conversation(item_id: str = Path(..., title="A unique ID string")):
    try:    
        result = delete_conversation_crud(item_id)
        if result.deleted_count==0:
            logging.info(f"Unable to find resource: {item_id}" )
            raise HTTPException(status_code=404, detail="Specified resource(s) was not found")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

@log_function
@app.post("/queries/{item_id}", status_code=201, summary="Creates a new Prompt query", description="This action sends a new Prompt query to the LLM and returns its response. If any errors occur when sending the prompt to the LLM, then a 422 error should be raised.")
async def create_prompt(prompt:KastomQuery,item_id: str = Path(..., title="A unique ID string")):
    try:    
        result = create_prompt_crud(prompt, item_id)
        if not result:
            logging.info(f"Unable to find resource: {item_id}" )
            raise HTTPException(status_code=404, detail="Specified resource(s) was not found")
    except ValueError as e:
        logging.info("An value error occurred:", e)
        raise HTTPException(status_code=400, detail="Invalid parameters provided")
    except Exception as e:
        logging.info(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")
