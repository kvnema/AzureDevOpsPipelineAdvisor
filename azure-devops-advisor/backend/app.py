import os
import json
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS
from flask_restx import Api, Resource, fields, reqparse
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from pathlib import Path

# Local imports
from utils.pipeline_analyzer import PipelineAnalyzer
from utils.azure_devops_client import AzureDevOpsClient

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

# Configure API
api = Api(
    app, 
    version='1.0', 
    title='Azure DevOps Pipeline Advisor API',
    description='API for analyzing Azure DevOps Pipelines',
    doc='/docs'
)

# Namespace for pipeline operations
ns = api.namespace('api/pipelines', description='Pipeline operations')

# Models
pipeline_model = api.model('Pipeline', {
    'id': fields.String(required=True, description='Pipeline ID'),
    'name': fields.String(required=True, description='Pipeline name'),
    'type': fields.String(description='Pipeline type (build/release)'),
    'url': fields.Url(description='Pipeline URL')
})

analysis_model = api.model('Analysis', {
    'status': fields.String(required=True, description='Analysis status'),
    'analysis': fields.Raw(description='Analysis results'),
    'recommendations': fields.List(fields.String, description='List of recommendations')
})

# User storage (in production, use a database)
users = {
    "admin": {
        "username": "admin",
        "password": generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin')),
        "role": "admin"
    }
}

# Authentication
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username]['password'], password):
        g.user = users[username]
        return True
    return False

# Initialize Azure DevOps client
def get_azure_devops_client():
    org = os.getenv('AZURE_DEVOPS_ORG')
    pat = os.getenv('AZURE_DEVOPS_PAT')
    
    if not org or not pat:
        raise ValueError("Azure DevOps organization and PAT must be configured")
        
    return AzureDevOpsClient(organization=org, personal_access_token=pat)

@ns.route('/analyze')
class PipelineAnalyzerResource(Resource):
    @api.expect(api.model('PipelineYAML', {
        'yaml_content': fields.String(required=True, description='YAML content to analyze')
    }))
    @api.response(200, 'Analysis completed', analysis_model)
    @api.response(400, 'Invalid YAML')
    def post(self):
        """Analyze Azure Pipeline YAML configuration"""
        try:
            # Get and validate request data
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return {'status': 'error', 'message': 'Invalid request data'}, 400
                
            yaml_content = data.get('yaml_content')
            if not yaml_content or not isinstance(yaml_content, str):
                return {'status': 'error', 'message': 'YAML content is required and must be a string'}, 400
            
            print(f"Received YAML content: {yaml_content[:100]}...")  # Debug log
            
            # Analyze the pipeline
            analyzer = PipelineAnalyzer(yaml_content=yaml_content)
            result = analyzer.analyze()
            
            print(f"Analysis result: {result}")  # Debug log
            
            # Handle the analysis result
            if result.get('status') == 'error':
                # Return the full error details from the analyzer
                return {
                    'status': 'error',
                    'message': result.get('message', 'Analysis failed'),
                    'details': result
                }, 400
                
            return result
            
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"Unexpected error in /analyze endpoint: {tb}")
            return {
                'status': 'error',
                'message': 'Failed to process request',
                'error': str(e),
                'traceback': tb
            }, 500

@ns.route('/list')
class PipelineListResource(Resource):
    @auth.login_required
    @api.marshal_list_with(pipeline_model)
    @api.response(401, 'Unauthorized')
    def get(self):
        """List all pipelines from Azure DevOps"""
        try:
            client = get_azure_devops_client()
            projects = client.get_projects()
            
            all_pipelines = []
            for project in projects:
                project_pipelines = client.get_pipelines(project['name'])
                all_pipelines.extend(project_pipelines)
                
            return all_pipelines
            
        except Exception as e:
            return {'error': f'Error fetching pipelines: {str(e)}'}, 500

@ns.route('/<string:project_name>/<int:pipeline_id>/yaml')
class PipelineYAMLResource(Resource):
    @auth.login_required
    @api.response(200, 'YAML content retrieved')
    @api.response(404, 'Pipeline not found')
    def get(self, project_name, pipeline_id):
        """Get YAML content of a pipeline"""
        try:
            client = get_azure_devops_client()
            yaml_content = client.get_pipeline_yaml(project_name, str(pipeline_id))
            
            if yaml_content is None:
                return {'error': 'YAML content not found for this pipeline'}, 404
                
            return {'yaml_content': yaml_content}
            
        except Exception as e:
            return {'error': f'Error fetching pipeline YAML: {str(e)}'}, 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def server_error(error):
    return {'error': 'Internal server error'}, 500

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_BUILD_DIR, path)):
        return send_from_directory(FRONTEND_BUILD_DIR, path)
    else:
        return send_from_directory(FRONTEND_BUILD_DIR, 'index.html')

if __name__ == '__main__':
    # Set up frontend build directory
    FRONTEND_BUILD_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'frontend', 'build'
    ))
    
    # Create default admin user if not exists
    if 'admin' not in users:
        users['admin'] = {
            'username': 'admin',
            'password': generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin')),
            'role': 'admin'
        }
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
