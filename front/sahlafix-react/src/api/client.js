import axios from "axios";

const http = axios.create({
  baseURL: "http://localhost:5000/api/v1", // cambia puerto si tu Flask usa otro
  headers: {
    "Content-Type": "application/json",
  },
});

// interceptor para añadir token si existe
http.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default http;