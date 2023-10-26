# Recipe-blog

This project was an exercise in building web applications using the Flask web framework, the SQLAlchemy ORM (Object-Relational Mapping) library, Bootstrap, and REST API calls. 
It allows users to view posted recipes, create an account, upload a user image, add recipes to their favorites list, 
and upload their own recipes along with recipe images and later update or delete their own recipe posts.

To install:
Clone the repository
git clone https://github.com/lmais/Recipe-blog.git

Navigate to the project directory
cd Recipe-blog

Install the dependencies
pip install -r requirements.txt
 
Set up the database:
Create a PostgreSQL database and update the config.py file with your database connection details.

Run the application:
flask run

The application will be accessible at `http://localhost:5000`.

Project Structure
The project has the following structure:

├── app

│   ├── models.py        # Database models

│   ├── routes.py        # Application routes

│   ├── templates        # HTML templates

│   └── __init__.py      # Application initialization

├── config.py            # Configuration settings

├── requirements.txt     # Project dependencies

└── run.py               # Entry point for running the application
