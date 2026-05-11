# My FastAPI Learning App

Small demo project for learning clean FastAPI structure.

## Run

```bash
uvicorn app.main:app --reload
```

Or:

```bash
python run.py
```

## Learn Flow

1. Request enters `app/main.py`
2. Router in `app/api/v1/router.py` sends request to endpoint
3. Endpoint uses dependency from `app/api/deps.py`
4. Service handles business logic
5. Repository reads or writes data
6. Schema controls request and response shape
