import http from "./http";

// registro
export const registerUser = async (payload) => {
  const { data } = await http.post("/auth/register", payload);
  return data;
};

// login
export const loginUser = async (payload) => {
  const { data } = await http.post("/auth/login", payload);

  if (data.token) {
    localStorage.setItem("token", data.token);
  }

  return data;
};