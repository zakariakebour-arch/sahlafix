import http from "./http";

export const getTechnicians = async () => {
  const { data } = await http.get("/technicians/");
  return data;
};

export const getTechnicianById = async (id) => {
  const { data } = await http.get(`/technicians/${id}`);
  return data;
};

export const createTechnician = async (payload) => {
  const { data } = await http.post("/technicians/", payload);
  return data;
};