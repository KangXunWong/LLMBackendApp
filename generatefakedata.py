from datetime import datetime
from uuid import uuid4
from models import baseConversation, Conversation, Message, Choices, Usage, KastomQuery, ChatCompletion
from db import chatresponsecollection

def generate_sample_data():
    """Generates sample data for multiple documents."""
    documents = []
    for i in range(10):  # Generate 10 documents
        conversation_id = str(uuid4())
        user_query = KastomQuery(role="user", content=f"Query {i}", additionalProp1={})
        choices = [
            Choices(index=0, message=Message(content=f"Response {i}", role='system',), logprobs={}, finish_reason="stop")
        ]
        usage = Usage(prompt_tokens=100, completion_tokens=50, total_tokens=150, completion_tokens_details={})
        chat_completion = ChatCompletion(
            uuid=str(uuid4()),
            id=conversation_id,
            name="Sample Conversation",
            params={},
            additionalProp1={},
            user_queries=[user_query],
            object="chat_completion",
            created=int(datetime.now().timestamp()),
            model="gpt-4o-mini",
            system_fingerprint="system_fingerprint",
            choices=choices,
            usage=usage
        )
        documents.append(chat_completion.dict())
    return documents

def insert_documents(documents):
    """Inserts a list of documents into the MongoDB collection."""
    try:
        result = chatresponsecollection.insert_many(documents)
        print("Documents inserted successfully:", result.inserted_ids)
    except Exception as e:
        print("Error inserting documents:", e)

if __name__ == "__main__":
    documents = generate_sample_data()
    insert_documents(documents)