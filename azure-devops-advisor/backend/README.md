# Azure DevOps Pipeline Advisor - Backend

This is the backend service for the Azure DevOps Pipeline Advisor, built with Flask.

## Local Development

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your Azure DevOps credentials and settings.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**:
   ```bash
   flask run
   ```
   The API will be available at `http://localhost:5000`

## Deployment to Render

1. **Create a new Web Service** on Render and connect your GitHub repository.

2. **Configure the following environment variables** in the Render dashboard:
   - `PYTHON_VERSION`: 3.9.0
   - `FLASK_APP`: backend/app.py
   - `FLASK_ENV`: production
   - `SECRET_KEY`: [Generate a secure random string]
   - `AZURE_DEVOPS_ORG`: Your Azure DevOps organization name
   - `AZURE_DEVOPS_PAT`: Your Azure DevOps Personal Access Token
   - `ADMIN_PASSWORD`: Set a secure admin password

3. **Build Command**:
   ```
   pip install -r requirements.txt
   ```

4. **Start Command**:
   ```
   gunicorn backend.app:app
   ```

## API Documentation

Once running, access the interactive API documentation at `/docs` (e.g., `http://localhost:5000/docs`).

## Environment Variables

- `AZURE_DEVOPS_ORG`: Your Azure DevOps organization name
- `AZURE_DEVOPS_PAT`: Your Azure DevOps Personal Access Token
- `FLASK_APP`: Entry point of the application
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Secret key for session management
- `ADMIN_PASSWORD`: Password for the default admin user
