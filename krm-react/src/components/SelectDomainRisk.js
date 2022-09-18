import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";

function SelectDomainRisk({selectedDomainRisks, setSelectedDomainRisks}) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [domainRisks, setDomainRisks] = useState([]);

  const handleOnChange = (pk) => {
    if (selectedDomainRisks.includes(pk)) {
      setSelectedDomainRisks(selectedDomainRisks.filter(item => item !== pk));
    } else {
      setSelectedDomainRisks(selectedDomainRisks.concat([pk]));
    }
  };

  useEffect(() => {
    fetch(`${configService.apiGetDomainRisks}`)
      .then((res) => res.json())
      .then(
        (res) => {
          setDomainRisks(res.results);
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
    return <div>Cargando dominios de riesgo...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <h5 className="mb-6">Seleccione Dominios de Riesgo</h5>
            {domainRisks.map((value, index) => {
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

export default SelectDomainRisk;
