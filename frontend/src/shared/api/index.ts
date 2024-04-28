import Axios from 'axios';

const BACKEND_URL = 'http://localhost:8000/v1';

export const axios = Axios.create({
  baseURL: BACKEND_URL,
});
