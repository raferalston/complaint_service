from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse


mock_app = FastAPI()
API_KEY = "mock-api-key"
MAX_TEXT_LENGTH = 2000


@mock_app.post("/v1/sentiment")
async def sentiment_analysis(
    request: Request,
    apikey: str = Header(None)):

    if apikey != f"{API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    body_bytes = await request.body()
    text = body_bytes.decode("utf-8")

    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="text parameter is required")

    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=413, detail="text too long – maximum 2000 characters")

    sentiment_result = {
        "POSITIVE": 0.8,
        "WEAK_POSITIVE": 0.4,
        "NEUTRAL": 0.0,
        "WEAK_NEGATIVE": -0.4,
        "NEGATIVE": -0.8
    }

    text_lower = text.lower()
    if "good" in text_lower or "love" in text_lower:
        sentiment = "POSITIVE"
    elif "bad" in text_lower or "hate" in text_lower:
        sentiment = "NEGATIVE"
    elif "ok" in text_lower or "fine" in text_lower:
        sentiment = "WEAK_POSITIVE"
    else:
        sentiment = "NEUTRAL"

    return {
        "score": sentiment_result[sentiment],
        "text": text,
        "sentiment": sentiment
    }


@mock_app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
