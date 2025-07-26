import os
import requests
from typing import List, Dict, Optional

class AzureDevOpsClient:
    """Client for interacting with Azure DevOps REST API."""
    
    BASE_URL = "https://dev.azure.com"
    
    def __init__(self, organization: str, personal_access_token: str):
        """Initialize the Azure DevOps client.
        
        Args:
            organization: Azure DevOps organization name
            personal_access_token: Azure DevOps Personal Access Token (PAT)
        """
        self.organization = organization
        self.personal_access_token = personal_access_token
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create and configure a requests session with authentication."""
        session = requests.Session()
        session.auth = ('', self.personal_access_token)  # Empty username, PAT as password
        session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json;api-version=6.0'
        })
        return session
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make an authenticated request to the Azure DevOps API."""
        url = f"{self.BASE_URL}/{self.organization}/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_projects(self) -> List[Dict]:
        """Get all projects in the organization."""
        endpoint = "_apis/projects?$top=1000"
        data = self._make_request('GET', endpoint)
        return data.get('value', [])
    
    def get_pipelines(self, project: str) -> List[Dict]:
        """Get all build and release pipelines in a project.
        
        Args:
            project: The name or ID of the project
            
        Returns:
            List of pipeline definitions
        """
        # Get build pipelines
        build_endpoint = f"{project}/_apis/build/definitions?api-version=6.0"
        build_pipelines = self._make_request('GET', build_endpoint).get('value', [])
        
        # Get release pipelines
        release_endpoint = f"{project}/_apis/release/definitions?api-version=6.0"
        release_pipelines = self._make_request('GET', release_endpoint).get('value', [])
        
        # Format and combine results
        pipelines = []
        
        for pipeline in build_pipelines:
            pipelines.append({
                'id': pipeline.get('id'),
                'name': pipeline.get('name'),
                'type': 'build',
                'url': pipeline.get('_links', {}).get('web', {}).get('href'),
                'createdDate': pipeline.get('createdDate'),
                'authoredBy': pipeline.get('authoredBy', {}).get('displayName')
            })
            
        for pipeline in release_pipelines:
            pipelines.append({
                'id': pipeline.get('id'),
                'name': pipeline.get('name'),
                'type': 'release',
                'url': pipeline.get('_links', {}).get('web', {}).get('href'),
                'createdDate': pipeline.get('createdOn'),
                'authoredBy': pipeline.get('createdBy', {}).get('displayName')
            })
            
        return pipelines
    
    def get_pipeline_yaml(self, project: str, pipeline_id: str, branch: str = 'main') -> Optional[str]:
        """Get the YAML content of a pipeline.
        
        Args:
            project: The name or ID of the project
            pipeline_id: The ID of the pipeline
            branch: The branch to get the YAML from
            
        Returns:
            The YAML content as a string, or None if not found
        """
        endpoint = f"{project}/_apis/build/definitions/{pipeline_id}?api-version=6.0"
        
        try:
            pipeline = self._make_request('GET', endpoint)
            
            # If the pipeline has a YAML file path, fetch its content
            if 'yamlFilename' in pipeline.get('process', {}):
                yaml_path = pipeline['process']['yamlFilename']
                # Get the YAML file content from the repository
                repo_id = pipeline.get('repository', {}).get('id')
                if repo_id:
                    file_content = self._get_file_content(project, repo_id, yaml_path, branch)
                    return file_content
            
            return None
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    def _get_file_content(self, project: str, repository_id: str, path: str, branch: str) -> Optional[str]:
        """Get the content of a file from a repository."""
        endpoint = f"{project}/_apis/git/repositories/{repository_id}/items?path={path}&versionDescriptor.version={branch}&api-version=6.0"
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/{self.organization}/{endpoint}",
                headers={'Accept': 'text/plain'}
            )
            response.raise_for_status()
            return response.text
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
