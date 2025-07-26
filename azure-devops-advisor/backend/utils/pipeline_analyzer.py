import yaml
from typing import Dict, List, Any


class PipelineAnalyzer:
    def __init__(self, yaml_content: str):
        self.yaml_content = yaml_content
        self.pipeline = {}

    def analyze(self) -> Dict:
        """Analyze a pipeline YAML configuration and return analysis results."""
        try:
            if not self.yaml_content or not isinstance(self.yaml_content, str):
                return {
                    'status': 'error',
                    'message': 'YAML content must be a non-empty string'
                }

            yaml_str = self.yaml_content.strip()
            if not yaml_str:
                return {'status': 'error', 'message': 'Empty YAML content'}

            try:
                pipeline_data = yaml.safe_load(yaml_str)
                if not pipeline_data or not isinstance(pipeline_data, dict):
                    return {'status': 'error', 'message': 'Invalid YAML structure'}

                self.pipeline = pipeline_data

                analysis = self._perform_analysis()
                return {
                    'status': 'success',
                    'analysis': analysis,
                    'recommendations': self._generate_recommendations(analysis)
                }

            except yaml.YAMLError as e:
                return {'status': 'error', 'message': f'Invalid YAML: {str(e)}'}

        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error in pipeline analysis: {str(e)}',
                'debug': {
                    'error_type': type(e).__name__,
                    'yaml_sample': str(self.yaml_content)[:100] + '...' if self.yaml_content else 'empty'
                }
            }

    def _perform_analysis(self) -> Dict:
        return {
            'stages': self._analyze_stages(),
            'jobs': self._analyze_jobs(),
            'security': self._analyze_security(),
            'best_practices': self._analyze_best_practices()
        }

    def _analyze_stages(self) -> Dict:
        if not isinstance(self.pipeline, dict):
            return {'count': 0, 'names': []}

        stages = self.pipeline.get('stages', [])
        if not isinstance(stages, list):
            stages = []

        stage_names = []
        for i, stage in enumerate(stages, 1):
            if isinstance(stage, dict):
                stage_name = stage.get('stage') or stage.get('displayName', f'stage_{i}')
                if isinstance(stage_name, str):
                    stage_names.append(stage_name)

        return {
            'count': len(stage_names),
            'names': stage_names
        }

    def _analyze_jobs(self) -> Dict:
        if not isinstance(self.pipeline, dict):
            return {'total': 0, 'types': []}

        stages = self.pipeline.get('stages', [])
        job_count = 0
        job_types = set()

        for stage in stages:
            if not isinstance(stage, dict):
                continue
            jobs = stage.get('jobs', [])
            if not isinstance(jobs, list):
                continue

            for job in jobs:
                if isinstance(job, dict):
                    job_count += 1
                    job_name = job.get('job') or job.get('displayName', 'unnamed')
                    if isinstance(job_name, str):
                        job_types.add(job_name)

        return {
            'total': job_count,
            'types': list(job_types)
        }

    def _analyze_security(self) -> Dict:
        if not isinstance(self.yaml_content, str):
            return {
                'has_secrets': False,
                'has_inline_scripts': False,
                'uses_secure_files': False,
                'has_approvals': False,
                'has_variable_groups': False
            }

        content_str = self.yaml_content.lower()
        return {
            'has_secrets': any(term in content_str for term in ['secret', 'token', 'password', 'key']),
            'has_inline_scripts': 'script:' in content_str,
            'uses_secure_files': any(term in content_str for term in ['securefile', 'securefile@']),
            'has_approvals': any(term in content_str for term in ['approvals:', 'reviewers:']),
            'has_variable_groups': 'variablegroup' in content_str
        }

    def _analyze_best_practices(self) -> Dict:
        if not isinstance(self.yaml_content, str):
            return {
                'has_testing': False,
                'has_artifacts': False,
                'uses_templates': False,
                'has_timeout': False,
                'has_retry': False,
                'has_parallelism': False
            }

        content_str = self.yaml_content.lower()
        return {
            'has_testing': any(term in content_str for term in ['test', 'pytest', 'unittest']),
            'has_artifacts': any(term in content_str for term in ['publish', 'artifact']),
            'uses_templates': 'template:' in content_str,
            'has_timeout': 'timeoutinminutes:' in content_str,
            'has_retry': 'retrycountontaskfailure:' in content_str,
            'has_parallelism': any(term in content_str for term in ['parallel:', 'matrix:'])
        }

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        if not isinstance(analysis, dict):
            return ["Unable to analyze pipeline: invalid analysis data"]

        recommendations = []
        security = analysis.get('security', {})
        best_practices = analysis.get('best_practices', {})

        # Stage-related recommendations
        if not isinstance(analysis.get('stages'), dict):
            recommendations.append("Unable to analyze pipeline stages.")
        else:
            stage_count = analysis['stages'].get('count', 0)
            if stage_count == 0:
                recommendations.append("Consider adding stages to organize your pipeline into logical sections.")
            elif stage_count < 2:
                recommendations.append("Consider separating your pipeline into multiple stages (e.g., build, test, deploy).")

        # Security recommendations
        if not security.get('has_secrets', True):
            recommendations.append("No secrets management detected. Consider using Azure Key Vault or pipeline variables.")
        
        if security.get('has_inline_scripts', False):
            recommendations.append("Consider moving inline scripts to separate script files for better maintainability.")
            
        if not security.get('has_approvals', False):
            recommendations.append("Consider adding approval gates for production deployments.")
            
        if not security.get('has_variable_groups', False):
            recommendations.append("Consider using variable groups for managing environment-specific configurations.")

        # Best practices recommendations
        if not best_practices.get('has_testing', True):
            recommendations.append("Add automated testing to ensure code quality.")

        if not best_practices.get('has_artifacts', True):
            recommendations.append("Consider publishing build artifacts for better traceability.")
            
        if not best_practices.get('uses_templates', False):
            recommendations.append("Consider using templates for reusable pipeline components.")
            
        if not best_practices.get('has_timeout', False):
            recommendations.append("Consider adding timeout limits to prevent long-running pipelines.")
            
        if not best_practices.get('has_retry', False):
            recommendations.append("Consider adding retry logic for flaky tasks.")
            
        if not best_practices.get('has_parallelism', False):
            recommendations.append("Consider using parallel jobs to speed up your pipeline execution.")

        return recommendations if recommendations else ["Your pipeline follows many best practices. Great job!"]
