import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  List, 
  ListItem, 
  ListItemText, 
  ListItemSecondaryAction, 
  IconButton,
  Paper,
  Divider,
  CircularProgress,
  Chip
} from '@mui/material';
import { 
  Visibility as VisibilityIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

const PipelineList = () => {
  const [pipelines, setPipelines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchPipelines = async () => {
    setLoading(true);
    setError('');
    
    try {
      // In a real app, this would be an API call to your backend
      // const response = await axios.get('/api/pipelines/list');
      // setPipelines(response.data);
      
      // Mock data for now
      setTimeout(() => {
        setPipelines([
          { id: '1', name: 'CI/CD Pipeline', status: 'succeeded', lastRun: '2023-07-25T10:30:00Z' },
          { id: '2', name: 'Deployment Pipeline', status: 'failed', lastRun: '2023-07-24T15:45:00Z' },
          { id: '3', name: 'Test Pipeline', status: 'succeeded', lastRun: '2023-07-25T08:15:00Z' },
        ]);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('Failed to fetch pipelines');
      console.error('Fetch error:', err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPipelines();
  }, []);

  const handleRefresh = () => {
    fetchPipelines();
  };

  const getStatusChip = (status) => {
    const statusMap = {
      succeeded: { label: 'Succeeded', color: 'success' },
      failed: { label: 'Failed', color: 'error' },
      running: { label: 'Running', color: 'info' },
      default: { label: 'Unknown', color: 'default' }
    };

    const { label, color } = statusMap[status] || statusMap.default;
    return <Chip label={label} color={color} size="small" />;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <Paper elevation={2} sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Your Pipelines</Typography>
        <IconButton onClick={handleRefresh} disabled={loading}>
          <RefreshIcon />
        </IconButton>
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" p={3}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : pipelines.length === 0 ? (
        <Typography>No pipelines found</Typography>
      ) : (
        <List>
          {pipelines.map((pipeline, index) => (
            <React.Fragment key={pipeline.id}>
              <ListItem>
                <ListItemText
                  primary={pipeline.name}
                  secondary={`Last run: ${formatDate(pipeline.lastRun)}`}
                />
                <Box mr={2}>
                  {getStatusChip(pipeline.status)}
                </Box>
                <ListItemSecondaryAction>
                  <IconButton edge="end" aria-label="view">
                    <VisibilityIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
              {index < pipelines.length - 1 && <Divider component="li" />}
            </React.Fragment>
          ))}
        </List>
      )}
    </Paper>
  );
};

export default PipelineList;
