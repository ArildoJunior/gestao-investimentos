// FILE: frontend/src/services/api.ts

import axios from 'axios';

const api = axios.create({
  
  // prefixo /api à URL base
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api', // URL do seu backend FastAPI com prefixo
  
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;