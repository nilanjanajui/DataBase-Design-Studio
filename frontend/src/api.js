import axios from 'axios';

// ✅ Environment-based URL
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
axios.defaults.baseURL = BASE_URL;

// ─────────────────────────────────────────
// Session Management
// ─────────────────────────────────────────

// ✅ Store session ID in memory (per browser tab)
let currentSessionId = null;

export const setSessionId = (id) => {
  currentSessionId = id;
};

export const getSessionId = () => currentSessionId;

// ✅ Attach session ID to every request automatically
axios.interceptors.request.use((config) => {
  if (currentSessionId) {
    config.headers['X-Session-ID'] = currentSessionId;
  }
  return config;
});


// ─────────────────────────────────────────
// File Upload
// ─────────────────────────────────────────

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  try {
    const response = await axios.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    if (response.status === 200 && response.data?.message) {
      // ✅ Save the session ID returned by backend
      if (response.data.session_id) {
        setSessionId(response.data.session_id);
        console.log('Session started:', response.data.session_id);
      }
      return response.data.message;
    } else {
      throw new Error('Unexpected response from upload API');
    }
  } catch (error) {
    throw new Error(error.response?.data?.message || 'File upload failed');
  }
};


// ─────────────────────────────────────────
// Backend Workflow Steps
// ─────────────────────────────────────────

export const triggerBackendStep = async (stepName) => {
  const endpointMap = {
    ConvertToCSV: '/api/convert_to_csv',
    CleanModify: '/api/clean_modify',
    FDModified: '/api/fd_modified',
    KeyDetection: '/api/key_detection',
    NormalizeTable: '/api/normalize_table',
    DependencyPreservation: '/api/dependency_preservation',
    LosslessCheck: '/api/lossless_check',
    ERDiagram: '/api/generate_er_diagram',
  };

  const endpoint = endpointMap[stepName];
  if (!endpoint) {
    throw new Error('Invalid step name');
  }

  try {
    const response = await axios.post(endpoint);

    if (response.status < 200 || response.status >= 300) {
      throw new Error(`Server returned status ${response.status}`);
    }

    if (stepName === 'LosslessCheck') {
      if (response.data && typeof response.data.message === 'string') {
        return response.data.message;
      }
      if (response.data) return JSON.stringify(response.data);
      return 'Unexpected response from lossless check API';
    }

    if (response.data && typeof response.data.message === 'string') {
      return response.data.message;
    }

    throw new Error(`Invalid response from server on ${stepName}`);
  } catch (error) {
    throw new Error(error.response?.data?.message || `Failed to trigger ${stepName}`);
  }
};


// ─────────────────────────────────────────
// Fetch Backend Code
// ─────────────────────────────────────────

export const fetchCodeForStep = async (stepName) => {
  try {
    const response = await axios.get(`/api/code/${stepName}`);
    if (response.status === 200 && response.data?.code) {
      return response.data.code;
    } else {
      throw new Error('Invalid response when fetching code');
    }
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to fetch code');
  }
};


// ─────────────────────────────────────────
// Normalized Tables
// ─────────────────────────────────────────

export const fetchNormalizedTables = async () => {
  try {
    const response = await axios.get('/api/normalized_tables');
    if (response.status === 200 && Array.isArray(response.data.tables)) {
      return response.data.tables;
    }
    console.warn('Unexpected response shape for normalized tables:', response.data);
    return [];
  } catch (error) {
    console.error('Error fetching normalized tables:', error);
    return [];
  }
};

export const fetchTableData = async (tableName) => {
  try {
    const response = await axios.get(`/api/get_normalized_table/${tableName}`);
    if (response.status === 200 && response.data) {
      return response.data;
    }
    throw new Error('Invalid response fetching table data');
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch table data');
  }
};


// ─────────────────────────────────────────
// Dependency Preservation
// ─────────────────────────────────────────

export const checkDependencyPreservation = async (originalFDs, decomposedSchemas) => {
  try {
    const response = await axios.post(
      '/api/dependency_preservation',
      { originalFDs, decomposedSchemas },
      { headers: { 'Content-Type': 'application/json' } }
    );
    if (response.status === 200 && typeof response.data.message === 'string') {
      return response.data.message;
    }
    throw new Error('Invalid response from dependency preservation API');
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Dependency preservation check failed';
    console.error('Dependency preservation check failed:', errorMsg);
    throw new Error(errorMsg);
  }
};


// ─────────────────────────────────────────
// Lossless Check
// ─────────────────────────────────────────

export const triggerLosslessCheck = async () => {
  try {
    const response = await axios.post('/api/lossless_check');
    if (response.status === 200 && typeof response.data.message === 'string') {
      return response.data.message;
    }
    if (response.data) return JSON.stringify(response.data);
    return 'Unexpected response from lossless check API';
  } catch (error) {
    const msg = error.response?.data?.message || error.message || 'Lossless check failed';
    console.error('Lossless check API error:', msg);
    throw new Error(msg);
  }
};