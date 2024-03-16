# Backend for Tucon

Flask-based server that supports handling request from the Next.js front-end application. It provides access to the data persistance storage.

## Prerequisites

- Python 3.12 or higher

## Local development

```bash
pip install -r requirements.txt
python tucon_backend/app.py
```

To test using Docker:

```bash
docker run --rm --env-file .env -p 8080:8080 -it $(docker build -q .)
```

## Manual deploy to Google Cloud Run

1. Install Google Cloud CLI - https://cloud.google.com/sdk/docs/install-sdk
2. Run the following commands. Note that 'tucon-cce32' is the firebase projectID.

```
gcloud init
gcloud run deploy tuconbackend --region=us-east1 --source=.
```

## Useful links

Firebase project: https://console.firebase.google.com/u/0/project/tucon-cce32/overview
