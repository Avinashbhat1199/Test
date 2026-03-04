
# Address Book FastAPI

## Run locally

python -m venv venv
venv\Scripts\activate (Windows) OR source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Open: http://127.0.0.1:8000/docs

## Run Tests
pytest

## Run with Docker
docker build -t address-book-api .
docker run -p 8000:8000 address-book-api
