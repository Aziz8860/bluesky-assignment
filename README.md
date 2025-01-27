# Bluesky Assignment - Backend

### Getting Started
### 1. Set Up Python Environment

#### Using `uv` (Recommended)
Ensure you have `uv` installed:
```bash
pip install uv
```
Create a virtual environment and activate it:
```bash
uv venv .venv
.venv\Scripts\activate
```
Install the required libraries:
```bash
uv pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Copy the sample environment file and modify it:
```bash
cp .env.example .env
```
Edit `.env` with your configurations:
```dotenv
DB_USER=postgres
DB_PASSWORD=[YOUR_PASSWORD]
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pokemondb
FLASK_APP=PokemonAPI
```

### 3. Set Up the Database
```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

### 4. Scrape Pokémon (default limit will be 50)
```bash
flask scrape
```
### or, with limit
```bash
flask scrape --limit 10
```

### 5. Run the API Service
```bash
python run.py
```

### Tech Stack:
- Flask
- PostgreSQL

### Available Endpoints:
- GET `http://localhost:5000/api/pokemon`
- GET `http://localhost:5000/api/pokemon/paginated?page={page}&pageSize={pageSize}`
- GET `http://localhost:5000/api/pokemon/{pokemonID}`

### Technical Specs
<img src="https://github.com/user-attachments/assets/53bb9138-bcee-45dd-b487-1943bd5177f3" alt="technical spec 1" width="800"/>

<img src="https://github.com/user-attachments/assets/2ef42468-c1d1-45f2-a73d-e5f6c977d5d2" alt="technical spec 2" width="800"/>

<img src="https://github.com/user-attachments/assets/223108b9-622c-4130-96cd-3d40563e6ac1" alt="technical spec 3" width="800"/>

