from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
import uvicorn
from app.config import settings
from app.webhook import verify_webhook, handle_webhook
from app.worker import start_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await start_worker()
    yield
    # Shutdown (if needed)


app = FastAPI(title="Instagram Automation Bot", lifespan=lifespan)


@app.get("/webhook")
async def verify_webhook_endpoint(request: Request):
    """Verify webhook endpoint for Instagram"""
    # Get query parameters manually since Instagram uses dots in parameter names
    query_params = dict(request.query_params)
    hub_mode = query_params.get('hub.mode')
    hub_challenge = query_params.get('hub.challenge')
    hub_verify_token = query_params.get('hub.verify_token')

    if hub_mode == "subscribe" and hub_verify_token == settings.instagram_verify_token:
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def webhook_endpoint(request: Request):
    """Receive webhook events from Instagram"""
    body = await request.body()

    # Temporarily disable signature verification for testing
    # TODO: Fix signature verification
    # if not await verify_webhook(request, body):
    #     raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    print(f"Received webhook: {data}")  # Debug log
    await handle_webhook(data)

    # Respond quickly (<5s)
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
