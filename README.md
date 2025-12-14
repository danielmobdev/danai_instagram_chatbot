# Instagram Automation Bot

A production-ready Instagram automation bot using official Meta APIs, FastAPI, Redis, and Gemini AI.

## Features

- Webhook-based message reception
- Asynchronous queue processing
- AI-powered responses using Gemini
- Rate limiting and anti-spam protection
- Conversation context storage
- Scalable and stateless design

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your credentials
4. Run Redis server
5. Start the app: `python main.py`

## Environment Variables

- `INSTAGRAM_ACCESS_TOKEN`: Your Instagram Business/Creator access token
- `INSTAGRAM_VERIFY_TOKEN`: Webhook verification token
- `INSTAGRAM_APP_SECRET`: App secret for webhook verification
- `REDIS_URL`: Redis connection URL
- `GEMINI_API_KEY`: Google Gemini API key
- `RATE_LIMIT_PER_USER`: Messages per hour per user
- `SPAM_THRESHOLD`: Repeated message threshold

## Deployment

### Option 1: Google Cloud Run (Recommended)

1. **Install Google Cloud CLI** and authenticate:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Update deploy.sh** with your project ID:
   ```bash
   # Edit deploy.sh and replace "your-gcp-project-id"
   nano deploy.sh
   ```

3. **Deploy**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Get the service URL** from the output and note it for webhook configuration.

### Option 2: Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t instagram-bot .
   ```

2. **Run locally for testing**:
   ```bash
   docker run -p 8000:8000 --env-file .env instagram-bot
   ```

3. **Deploy to any container platform** (Render, Railway, etc.)

### Option 3: VPS Deployment

1. **Upload files** to your VPS
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run with environment variables**:
   ```bash
   export $(cat .env | xargs) && python main.py
   ```
4. **Use a process manager** like systemd or supervisor

### Webhook Configuration in Meta Developer Console

1. **Go to** [Meta Developer Console](https://developers.facebook.com/)
2. **Select your app** (ID: 918754297141613)
3. **Navigate to** Webhooks > Instagram
4. **Add webhook**:
   - **Callback URL**: `https://your-deployed-url.com/webhook`
   - **Verify Token**: `danai_ig_verify_123`
5. **Subscribe** to `messages` and `messaging_postbacks` events
6. **Test** the webhook to ensure it verifies successfully

### Environment Setup

Ensure Redis is available (Upstash recommended for serverless). All secrets are loaded from environment variables - never commit `.env` to git.

## API Endpoints

- `GET /webhook`: Webhook verification
- `POST /webhook`: Receive Instagram messages
- `GET /health`: Health check

## Architecture

- FastAPI handles webhooks (<5s response)
- Redis queue for async processing
- Background worker generates AI responses
- Instagram Graph API for sending messages
- All state stored in Redis
