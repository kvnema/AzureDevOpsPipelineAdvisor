import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import PipelineAnalyzer from './components/PipelineAnalyzer';
import PipelineList from './components/PipelineList';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#0078d4',
    },
    secondary: {
      main: '#ff8c00',
    },
  },
  typography: {
    fontFamily: '"Segoe UI", "Segoe UI Web (West European)", -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif',
    h4: {
      fontWeight: 600,
    },
  },
});

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Azure DevOps Pipeline Advisor
          </Typography>
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
            <Tabs 
              value={tabValue} 
              onChange={handleTabChange} 
              aria-label="Pipeline advisor tabs"
            >
              <Tab label="Analyze YAML" />
              <Tab label="Pipeline List" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <PipelineAnalyzer />
          </TabPanel>
          <TabPanel value={tabValue} index={1}>
            <PipelineList />
          </TabPanel>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
