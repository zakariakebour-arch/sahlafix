import { useEffect, useState } from "react";
import { getTechnicians } from "../api/technician";

export default function Home() {
  const [technicians, setTechnicians] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getTechnicians();
      setTechnicians(data);
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Technicians</h1>

      <ul>
        {technicians.map((t) => (
          <li key={t.id}>{t.name}</li>
        ))}
      </ul>
    </div>
  );
}