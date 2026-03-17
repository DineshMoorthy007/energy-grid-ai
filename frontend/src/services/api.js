import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const predictDemand = async (hour, temperature) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/predict`, {
      params: {
        hour,
        temp: temperature
      }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching prediction:", error);
    throw error;
  }
};
