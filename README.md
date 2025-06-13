create a virtiual environment 
python -m venv venv 
source venv/bin/activate

install dependencies using pip install -r requirements.txt

run the intial bd setup alembic upgrade head python src/scripts/init_db.py

To launch the application do python run.py or uvicorn src.main:app --reload to run the frontend do python server.py

To test services and repositories do pytest src/tests/...

To check the requirements check the requirements.txt file in the source of the project
