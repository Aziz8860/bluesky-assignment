from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    
    # Create database if it doesn't exist
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if the database exists and create it if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    from app.api.pokemon import pokemon_bp
    app.register_blueprint(pokemon_bp, url_prefix='/api/pokemon')
    
    # Register CLI commands
    from app.commands.scrape import scrape_cli
    app.cli.add_command(scrape_cli)
    
    return app