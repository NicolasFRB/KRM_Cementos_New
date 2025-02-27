import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectPlant({ selectedPlants, setSelectedPlants }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [plants, setPlants] = useState([]);

  const handleOnChange = (value) => {
    if (selectedPlants.includes(value)) {
      setSelectedPlants(selectedPlants.filter(item => item !== value));
    } else {
      setSelectedPlants(selectedPlants.concat([value]));
    }
  };

  const [t] = useTranslation("global");

  useEffect(() => {
    fetch(`${configService.apiGetPlants}`)
      .then((res) => res.json())
      .then(
        (res) => {
          console.log("Plants: ", res)
          setPlants(res);
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
    return <div>{t('controls.loading-controls')}...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <h5 className="mb-6">{t('general.loading-plant')}</h5>
            {plants.map((value, index) => {
              return <p key={value}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value)} className="form-check-input" name="plant" type="checkbox" value={value} />
                  <span className="fw-semibold ps-2 fs-6">{value}</span>
                </label>
              </p>
            })}
          </>
        )}
      </div>
    );
  }
}

export default SelectPlant;
