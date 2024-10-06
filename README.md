# Project Name

## Overview

This project is designed to provide a robust backend service for managing conversations and generating responses using OpenAI's GPT-4 model. The system is built with FastAPI and MongoDB, ensuring high performance and scalability.

## System Design

### Architecture

The system is composed of several key components:

1. **FastAPI Application**: The core of the backend service, handling HTTP requests and routing.
2. **MongoDB**: A NoSQL database used to store conversation data.
3. **OpenAI Integration**: Utilizes OpenAI's API to generate responses based on user queries.

### Key Modules

- **`main.py`**: Entry point of the application. Configures and starts the FastAPI server.
- **`routes.py`**: Defines the API endpoints and their respective handlers.
- **`services.py`**: Contains business logic for creating and updating conversations.
- **`db.py`**: Manages database connections and collections.
- **`settings.py`**: Configuration settings for the application, including environment variables.
- **`generatefakedata.py`**: Utility script for generating and inserting sample data into the database.
- **`log.py`**: Configures logging for the application.

### Data Models

The data models are defined in `models.py` and include:

- **`Conversation`**: Represents a conversation document.
- **`Message`**: Represents individual messages within a conversation.
- **`ChatCompletion`**: Represents the completion response from OpenAI.

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB
- OpenAI API Key

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/your-repo/project-name.git
   cd project-name
   ```

2. **Create and activate a virtual environment**:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   ENVIRONMENT=dev
   SECRET_KEY=your_secret_key
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o-mini
   DB_URL=your_mongodb_url
   DB_NAME=your_db_name
   BASE_URL=127.0.0.1
   PORT=8000
   ```

### Starting the Server

1. **Run the FastAPI server**:

   ```sh
   python main.py
   ```

   This will start the server at `http://127.0.0.1:8000`.

### Generating Sample Data

To generate and insert sample data into the MongoDB collection, run:

```sh
python generatefakedata.py
```

### Logging

Logging is configured via logging.ini. Logs are written to a file named with the current date in the format YYYY-MM-DD_Uvicorn.log.

### API Endpoints

- `POST /conversations`: Create a new conversation.
- `GET /conversations/{item_id}`: Retrieve a conversation by ID.
- `GET /conversations/{item_id}/history`: Retrieve the history of a conversation.
- `PUT /conversations/{item_id}`: Update a conversation by ID.
- `DELETE /conversations/{item_id}`: Delete a conversation by ID.
- `POST /conversations/{item_id}/prompts`: Add a prompt to an existing conversation.

### Limitations

- The `POST /conversations/{item_id}/prompts` API does not work as expected due to CORS issues when testing on an Ubuntu server.

### Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

### License

This project is licensed under the MIT License - see the LICENSE file for details. ```
