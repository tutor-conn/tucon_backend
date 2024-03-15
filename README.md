# Backend for Tucon

Flask-based server that supports handling request from the Next.js front-end application. It provides access to the data persistance storage.

## Setup steps
1. Clone the repo
2. Install Google Cloud CLI - https://cloud.google.com/sdk/docs/install-sdk

3. Run the following commands. Note that 'tucon-cce32' is the firebase projectID.
```
gcloud init
gcloud builds submit --tag gcr.io/tucon-cce32/tucon_backend
gcloud run deploy --image gcr.io/tucon-cce32/tucon_backend
```

## Useful links
Firebase project: https://console.firebase.google.com/u/0/project/tucon-cce32/overview