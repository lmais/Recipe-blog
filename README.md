# Recipe-blog

This project was an exercise in building web applications using the Flask web framework and the SQLAlchemy ORM (Object-Relational Mapping) library. 

To install:
Clone the repository
git clone https://github.com/your-username/your-repo.git

Navigate to the project directory
cd your-repo

Install the dependencies
pip install -r requirements.txt
_____________________
pip install flask-wtf 
pip install flask-bcrypt
pip install flask-login
pip install pillow

___________________
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
