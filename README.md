# Setup Instructions
## Introduction
This is a REST API for managing todo items. The API uses FastAPI as the web framework, Supabase as the database, and JWT for authentication.

## Prerequisites
* Python 3.9 or higher
* pip 22.0 or higher
* A Supabase instance
* A .env file with the following environment variables:
	+ SUPABASE_URL
	+ SUPABASE_KEY
	+ JWT_SECRET

## Installation
1. Clone the repository: `git clone https://github.com/your-username/todo-app.git`
2. Create a new .env file: `cp .env.example .env`
3. Fill in the environment variables in the .env file
4. Install the dependencies: `pip install -r requirements.txt`
5. Run the application: `uvicorn main:app --host 0.0.0.0 --port 8000`

## Environment Variables
The following environment variables are required:
* `SUPABASE_URL`: The URL of your Supabase instance
* `SUPABASE_KEY`: The key for your Supabase instance
* `JWT_SECRET`: The secret key for JWT authentication

## API Endpoints
The API has the following endpoints:
* `/users`: Create, read, update, and delete users
* `/todos`: Create, read, update, and delete todo items

## API Documentation
The API documentation is available at `http://localhost:8000/docs`

## Running Tests
To run the tests, use the following command: `pytest`

## Deployment
To deploy the application, use a WSGI server such as Gunicorn or uWSGI. You can also use a cloud platform such as Railway or Heroku.

## Contributing
To contribute to the project, please fork the repository and submit a pull request. Make sure to include tests for any new features or bug fixes.

## License
The project is licensed under the MIT License.