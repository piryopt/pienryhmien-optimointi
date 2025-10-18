import { baseUrl } from '../utils/constants';

const fetchCsrfToken = async () => {
  const res = await fetch(`${baseUrl}/csrf_token`, {
    credentials: 'include'
  });
  const data = await res.json();
  return data.csrfToken; 
};

export default {
  fetchCsrfToken: fetchCsrfToken
};