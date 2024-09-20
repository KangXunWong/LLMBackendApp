# Chat Application

This is a chat application built with FastAPI, MongoDB, and OpenAI's API. The application allows users to create, retrieve, update, and delete conversations, as well as create prompts within conversations.

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following environment variables:
     ```env
     ENVIRONMENT=development
     SECRET_KEY=your_secret_key
     OPENAI_API_KEY=your_openai_api_key
     OPENAI_MODEL=gpt-4o-mini
     DB_URL=your_mongodb_url
     DB_NAME=your_database_name
     BASE_URL=127.0.0.1
     PORT=8000
     ```

## Usage

1. Run the application:

   ```sh
   uvicorn main:app --reload
   ```

2. The application will be available at `http://127.0.0.1:8000`.

## Code Logic

### `main.py`

- The entry point of the application.
- Configures logging and starts the FastAPI server.

### `settings.py`

- Contains the `Settings` class which loads environment variables.

### `db.py`

- Sets up the MongoDB client and the OpenAI client.
- Provides access to the `chatresponsecollection` in MongoDB.

### `models.py`

- Defines the data models used in the application, such as `ChatCompletion`, `Choices`, `Message`, and `Usage`.

### `services.py`

- Contains CRUD operations for conversations and prompts.
- Functions include:
  - `create_conversation_crud`: Creates a new conversation and stores it in MongoDB.
  - `retrieve_conversation_crud`: Retrieves all conversations.
  - `update_conversation_crud`: Updates an existing conversation.
  - `retrieve_conversation_history`: Retrieves a conversation by its ID.
  - `delete_conversation_crud`: Deletes a conversation by its ID.
  - `create_prompt_crud`: Adds a prompt to an existing conversation.

### `log.py`

- Configures logging for the application.

### `logging.conf`

- Configuration file for logging, specifying loggers, handlers, and formatters.

### `Dockerfile`

- Docker configuration for containerizing the application.

### `requirements.txt`

- Lists all the dependencies required for the application.

## License

This project is licensed under the MIT License.
