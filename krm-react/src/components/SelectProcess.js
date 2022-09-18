import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";

function SelectProcess({selectedProcesses, setSelectedProcesses}) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [processes, setProcesses] = useState([]);

  const handleOnChange = (pk) => {
    if (selectedProcesses.includes(pk)) {
      setSelectedProcesses(selectedProcesses.filter(item => item !== pk));
    } else {
      setSelectedProcesses(selectedProcesses.concat([pk]));
    }
  };

  useEffect(() => {
    fetch(`${configService.apiGetProcesses}`)
      .then((res) => res.json())
      .then(
        (res) => {
          setProcesses(res.results);
          setIsLoaded(true);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, []);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Cargando controles...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <h5 className="mb-6">Seleccione Proceso</h5>
            {processes.map((value, index) => {
              return <p key={value.pk}>
                  <label className="form-check form-check-inline form-check-solid me-5">
                    <input onChange={() => handleOnChange(value.pk)} className="form-check-input" name="process" type="checkbox" value={value.pk} />
                    <span className="fw-semibold ps-2 fs-6">{value.name}</span>
                  </label>
                </p>
            })}
          </>
        )}
      </div>
    );
  }
}

export default SelectProcess;
