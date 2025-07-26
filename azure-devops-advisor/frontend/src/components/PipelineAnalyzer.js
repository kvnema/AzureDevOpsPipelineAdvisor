import React, { useState } from 'react';
import { 
  Box, 
  Button, 
  TextField, 
  Paper, 
  Typography, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText, 
  CircularProgress,
  Alert,
  Divider
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import axios from 'axios';

const PipelineAnalyzer = () => {
  const [yamlContent, setYamlContent] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!yamlContent.trim()) {
      setError('Please enter YAML content to analyze');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('/api/pipelines/analyze', {
        yaml_content: yamlContent
      });
      setAnalysis(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze pipeline');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleYamlChange = (event) => {
    setYamlContent(event.target.value);
    // Clear previous results when YAML changes
    if (analysis) setAnalysis(null);
    if (error) setError('');
  };

  return (
    <Box>
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Paste your Azure Pipeline YAML
        </Typography>
        <TextField
          fullWidth
          multiline
          rows={10}
          variant="outlined"
          placeholder="Paste your Azure Pipeline YAML here..."
          value={yamlContent}
          onChange={handleYamlChange}
          sx={{ mb: 2, fontFamily: 'monospace' }}
        />
        <Button 
          variant="contained" 
          color="primary" 
          onClick={handleAnalyze}
          disabled={loading || !yamlContent.trim()}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          {loading ? 'Analyzing...' : 'Analyze Pipeline'}
        </Button>
        
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {analysis && (
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Results
          </Typography>
          
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Pipeline Metrics
            </Typography>
            <List dense>
              <ListItem>
                <ListItemText 
                  primary={`Stages: ${analysis.analysis?.stages_count || 0}`} 
                />
              </ListItem>
              {analysis.analysis?.jobs_per_stage && Object.entries(analysis.analysis.jobs_per_stage).map(([stage, jobs]) => (
                <ListItem key={stage}>
                  <ListItemText 
                    primary={`Jobs in ${stage}: ${jobs}`} 
                    secondary={stage}
                  />
                </ListItem>
              ))}
            </List>
          </Box>

          <Divider sx={{ my: 2 }} />
          
          <Box>
            <Typography variant="subtitle1" gutterBottom>
              Recommendations
            </Typography>
            <List>
              {analysis.recommendations?.map((rec, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    {rec.includes('looks good') ? (
                      <CheckCircleIcon color="success" />
                    ) : (
                      <WarningIcon color="warning" />
                    )}
                  </ListItemIcon>
                  <ListItemText primary={rec} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Paper>
      )}
    </Box>
  );
};

export default PipelineAnalyzer;
