import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";

function SelectCompanies({ selectedCompanies, setSelectedCompanies, companies, setCompanies }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  const handleOnChange = (pk) => {
    if (selectedCompanies.includes(pk)) {
      setSelectedCompanies(selectedCompanies.filter(item => item !== pk));
    } else {
      setSelectedCompanies(selectedCompanies.concat([pk]));
    }
  };

  useEffect(() => {
    fetch(`${configService.apiGetCompanies}`)
      .then((res) => res.json())
      .then(
        (res) => {
          setCompanies(res);
          setIsLoaded(true);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, [setCompanies]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Cargando compañías...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            {companies.map((value, index) => {
              return <p key={value.pk}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value.pk)} className="form-check-input" name="process" type="checkbox" value={value.pk} />
                  <span className="fw-semibold ps-2 fs-6">{value.name}</span>
                </label>
              </p>
            })}
            <input type="hidden" name="companies" value={selectedCompanies} />
          </>
        )}
      </div>
    );
  }
}

export default SelectCompanies;
