# Azure DevOps Pipeline Advisor

A full-stack application for analyzing and optimizing Azure DevOps Pipelines.

## Deployment

This application can be deployed to any platform that supports Python applications. We recommend using [Render](https://render.com) or [Railway](https://railway.app) for easy deployment.

### Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm (for frontend build)
- Azure DevOps Personal Access Token (PAT) with appropriate permissions

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Azure DevOps Configuration
AZURE_DEVOPS_ORG=your-organization-name
AZURE_DEVOPS_PAT=your-personal-access-token

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Authentication
ADMIN_PASSWORD=admin

# CORS Configuration
FRONTEND_URL=https://your-production-url.com
```

### Local Development

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

4. Start the development servers:
   - Backend: `cd backend && flask run`
   - Frontend: `cd frontend && npm start`

### Production Deployment

1. Build the frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. Deploy to your preferred platform (Render, Railway, Heroku, etc.)

### Platform-Specific Instructions

#### Render

1. Create a new Web Service on Render
2. Connect your GitHub/GitLab repository
3. Set the following environment variables in the Render dashboard:
   - `PYTHON_VERSION`: 3.9.0
   - `NODE_VERSION`: 16.x
   - `INSTALL_COMMAND`: pip install -r requirements.txt && cd frontend && npm install && npm run build
   - `START_COMMAND`: gunicorn --bind 0.0.0.0:$PORT backend.app:app

#### Railway

1. Create a new project on Railway
2. Add a new service and select "Deploy from GitHub repo"
3. Select your repository
4. Add the environment variables from the `.env` file
5. Deploy!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


A full-stack application for analyzing and providing recommendations for Azure DevOps Pipelines.

## Features

- Analyze Azure Pipeline YAML configurations
- Get recommendations for pipeline improvements
- View pipeline execution history
- Integration with Azure DevOps API

## Prerequisites

- Python 3.8+
- Node.js 16+
- Azure DevOps organization and Personal Access Token (PAT)

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```
   AZURE_DEVOPS_ORG=your-organization
   AZURE_DEVOPS_PROJECT=your-project
   AZURE_DEVOPS_PAT=your-personal-access-token
   ```

5. Run the backend server:
   ```bash
   flask run --port=5000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

## API Endpoints

- `GET /api/pipelines/list` - List all pipelines
- `POST /api/pipelines/analyze` - Analyze pipeline YAML
  - Request body: `{ "yaml_content": "your yaml here" }`

## Project Structure

```
azure-devops-advisor/
├── backend/               # Flask backend
│   ├── app.py            # Main application
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables
└── frontend/             # React frontend
    ├── public/           # Static files
    └── src/              # React source code
```
