# flower_back

Backend for the flower catalog. By default, the project runs in mock mode and reads products from JSON so the frontend can test the catalog without PostgreSQL.

## Default mode

`USE_MOCK_DATA=true` is enabled by default. The API reads products from:

`backend/data/catalog.json`

Frontend developers can replace this file with their own JSON and test locally.

## Run locally

1. Create a virtual environment.
2. Install dependencies from `backend/requirements.txt`.
3. Copy `.env.example` to `.env` if you want to override defaults.
4. Start the backend from the `backend` folder with `uvicorn main:app --reload`.

Example on Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
Get-Content .env.example | Set-Content .env
cd backend
uvicorn main:app --reload
```

API will be available at `http://127.0.0.1:8000`.

## Frontend access

CORS is enabled for:

- `http://localhost:3000`
- `http://localhost:5173`

## Main endpoints

- `GET /health`
- `GET /flowers`
- `GET /flowers/{id}`

## Database mode

If you want to use PostgreSQL later:

1. Set `USE_MOCK_DATA=false`
2. Set `DATABASE_URL` in `.env`
3. Start PostgreSQL and run the backend

## GitHub safety

The project ignores:

- `.env`
- local virtual environments
- Python cache files

Do not commit real secrets to the repository.
