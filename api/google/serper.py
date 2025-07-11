import http
import json
import os
import dotenv
from fastapi import APIRouter, Query, HTTPException
from config import logger
from model.response import Response
from model.search_query import SearchQuery

dotenv.load_dotenv()

GOOGLE_SERPER_API_KEY = os.environ.get("GOOGLE_SERPER_API_KEY")

router = APIRouter(
    prefix="/google/serper",
    tags=["google_serper"],
    responses={404: {"description": "Not found"}},
)



@router.post("/search")
async def search(query: SearchQuery, api_key: str = GOOGLE_SERPER_API_KEY):
    logger.info("Received search request with query: {}", query)
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload_str = query.model_dump_json()  # Get JSON string
        payload = payload_str.encode('utf-8')  # Explicitly encode to UTF-8
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        decoded_data = data.decode("utf-8")
        conn.close()
        organic_data= json.loads(decoded_data).get("organic", [])
        return Response.success(
            data=organic_data
        )
    except Exception as e:
        logger.error(f"Error during API call: {str(e)}")
        return Response.error(
            code=500,
            message=f"Error during API call: {str(e)}",
            data=None
        )