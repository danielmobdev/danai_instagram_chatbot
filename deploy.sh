#!/bin/bash

# Deploy to Google Cloud Run
echo "Building and deploying to Cloud Run..."

# Set your project ID
PROJECT_ID="serenity-review-app"
SERVICE_NAME="instagram-bot"

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "INSTAGRAM_ACCESS_TOKEN=$INSTAGRAM_ACCESS_TOKEN" \
  --set-env-vars "INSTAGRAM_BUSINESS_ID=$INSTAGRAM_BUSINESS_ID" \
  --set-env-vars "INSTAGRAM_APP_ID=$INSTAGRAM_APP_ID" \
  --set-env-vars "INSTAGRAM_VERIFY_TOKEN=$INSTAGRAM_VERIFY_TOKEN" \
  --set-env-vars "INSTAGRAM_APP_SECRET=$INSTAGRAM_APP_SECRET" \
  --set-env-vars "REDIS_URL=$REDIS_URL" \
  --set-env-vars "GEMINI_API_KEY=$GEMINI_API_KEY"

echo "Deployment complete! Get the service URL:"
gcloud run services describe $SERVICE_NAME --region=us-central1 --format="value(status.url)"
