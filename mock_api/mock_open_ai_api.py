from fastapi import FastAPI, Header, HTTPException, Request


mock_app = FastAPI()
API_KEY = "mock-api-key"


@mock_app.post("/v1/chat/completions")
async def mock_openai_api(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    body = await request.json()

    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Missing messages")

    user_message = messages[0].get("content", "")

    if "!оплата" in user_message.lower():
        category = "оплата"
    elif "!техническая" in user_message.lower():
        category = "техническая"
    else:
        category = "другое"

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": category
                }
            }
        ]
    }
