# Development Setup

## 1. Create the virtual environment with uv

Install `uv` first if it is not already installed on your machine.

Example:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

From the project root, create a virtual environment:
```bash
uv venv
```

Activate it:

### macOS / Linux
```bash
source .venv/bin/activate
```

### Windows PowerShell
```powershell
.venv\Scripts\Activate.ps1
```

## 2. Install packages from requirements.txt

With the virtual environment activated, install dependencies using:
```bash
uv pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, create it first and list the initial packages needed for the MVP, such as:
- fastapi
- uvicorn
- pandas
- pydantic
- python-dotenv
- sqlalchemy
- psycopg2-binary
- streamlit
- httpx
- langdetect or lingua-language-detector
- pytest

## 3. Set up `.env`

Create a file named `.env` in the project root:
```bash
touch .env
```

Add environment variables similar to the following:
```env
APP_ENV=local
APP_HOST=127.0.0.1
APP_PORT=8000

DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/bilingual_annotation

HF_API_KEY=your_huggingface_api_key
HF_MODEL_ID=your_selected_model_id

LOG_LEVEL=INFO
```

## 4. Add an `.env.example`

Create a tracked template file named `.env.example` that includes the required keys without secrets:
```env
APP_ENV=local
APP_HOST=127.0.0.1
APP_PORT=8000
DATABASE_URL=
HF_API_KEY=
HF_MODEL_ID=
LOG_LEVEL=INFO
```

## 5. Load environment variables in the app

Use `python-dotenv` in your configuration layer so local development automatically loads values from `.env`.

Example approach:
- create `app/core/config.py`
- load `.env`
- expose typed settings through Pydantic or a small settings class

## 6. Basic local startup sequence

Planned local startup order:
1. start Postgres
2. activate the virtual environment
3. install or update dependencies
4. confirm `.env` values are present
5. run the FastAPI app
6. run the Streamlit review UI in a separate terminal

## 7. Notes

- Do not commit the real `.env` file.
- Add `.env` and `.venv/` to `.gitignore`.
- Keep secrets limited to local development in the MVP.
- Prefer a single source of configuration truth through `config.py`.
