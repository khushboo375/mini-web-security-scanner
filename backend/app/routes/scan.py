from fastapi import APIRouter
from app.services.scanner import run_scan

router = APIRouter()

@router.post("/scan")
async def scan_url(data: dict):
    url = data.get("url")

    result = run_scan(url)

    return {
        "status": "completed",
        "data": result
    }