# README

## Project Overview

This is a simple chat application built using Flask, Flask-SocketIO, and SQLite. The application allows users to create or join chat rooms, send messages, and view chat history.

## Requirements

* Python 3.8+
* Flask 2.0+
* Flask-SocketIO 5.0+
* Flask-CORS 3.0+
* SQLite 3.0+

## Installation

1. Clone the repository: `git clone https://github.com/your-username/your-repo-name.git`
2. Navigate to the project directory: `cd your-repo-name`
3. Install the required dependencies: `pip install -r requirements.txt`

## Running the Application

1. Run the application: `python app.py`
2. Open a web browser and navigate to `http://localhost:5000`

## Features

* Create or join chat rooms
* Send messages to other users in the same room
* View chat history for each room
* Leave a room and return to the home page

## API Endpoints

* `/`: Home page
* `/room`: Chat room page
* `/get_chat_history/<room_code>`: Get chat history for a specific room
* `/get_room_users/<room_code>`: Get a list of users in a specific room
* `/leave`: Leave a room and return to the home page

## SocketIO Events

* `message`: Send a message to other users in the same room
* `connect`: Connect to a room and join the chat
* `disconnect`: Leave a room and disconnect from the chat

## Database

The application uses a SQLite database to store chat history and room information. The database is created automatically when the application is run for the first time.

## Troubleshooting

* If you encounter any issues with the application, check the console output for error messages.
* Make sure that the SQLite database file is not corrupted or deleted.

## Contributing

Contributions to the project are welcome. Please submit a pull request with your changes and a brief description of what you've done.

**Docker**

* Build the Docker image: `docker build -t chat-room .`
* Run the container: `docker run -p 5000:5000 chat-room`
