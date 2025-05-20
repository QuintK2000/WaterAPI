# main.py
import os
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI()
df = pd.read_csv("water_potability.csv")

# Allow CORS for all origins (optional but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/data/water-potability")
async def get_metadata(request: Request):
    verify_token(request)
    return {
        "columns": list(df.columns),
        "row_count": len(df),
        "description": "Water Potability Dataset"
    }

@app.get("/data/water-potability/download")
async def download_file(request: Request):
    verify_token(request)
    return FileResponse("water_potability.csv", media_type='text/csv', filename="water_potability.csv")

@app.get("/data/water-potability/preview")
async def preview_data(request: Request):
    verify_token(request)
    preview_df = df.head(5).replace({np.nan: None, np.inf: None, -np.inf: None})
    return preview_df.to_dict(orient="records")

