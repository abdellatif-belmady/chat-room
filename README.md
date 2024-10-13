# Chat Room

Chat Room is an open-source real-time chat application built with Flask and Socket.IO. It allows users to create or join chat rooms and communicate in real-time.

## Features

- Create and join chat rooms
- Real-time messaging
- Persistent chat history using SQLite
- User join/leave notifications
- Dockerized application for easy deployment

## Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/abdellatif-belmady/chat-room.git
   cd chat-room
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

### Local Development

To run the application locally:

```
python app.py
```

The application will be available at `http://localhost:5000`.

### Docker Deployment

To run the application using Docker:

1. Build the Docker image:
   ```
   docker build -t chat-room .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 chat-room
   ```

The application will be available at `http://localhost:5000`.

## Project Structure

- `app.py`: Main Flask application file
- `templates/`: Directory for HTML templates
  - `home.html`: Home page template
  - `room.html`: Chat room template
- `static/`: Directory for static files (CSS, JavaScript)
- `Dockerfile`: Instructions for building the Docker image
- `requirements.txt`: List of Python dependencies

## API Endpoints

- `GET /`: Home page
- `POST /`: Create or join a room
- `GET /room`: Chat room page
- `GET /get_chat_history/<room_code>`: Get chat history for a room
- `GET /get_room_users/<room_code>`: Get list of users in a room
- `GET /leave`: Leave the current room

## WebSocket Events

- `message`: Send and receive messages
- `connect`: User connects to a room
- `disconnect`: User disconnects from a room

## Database

The application uses SQLite for persisting chat messages and room information. The database file `chat.db` is created automatically when the application runs for the first time.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

This project was created by [Abdellatif BELMADY](https://abdellatif-belmady.github.io/abdellatif-belmady/).
