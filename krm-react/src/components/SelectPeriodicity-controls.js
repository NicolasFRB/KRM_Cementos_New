import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectPeriodicity({ selectedPeriodicity, setSelectedPeriodicity }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [periodicity, setPeriodicity] = useState([]);

  const handleOnChange = (pk) => {
    if (selectedPeriodicity.includes(pk)) {
      setSelectedPeriodicity(selectedPeriodicity.filter(item => item !== pk));
    } else {
      setSelectedPeriodicity(selectedPeriodicity.concat([pk]));
    }
  };

  const [t] = useTranslation("global");

  useEffect(() => {
    fetch(`${configService.apiGetControls}`)
      .then((res) => res.json())
      .then(
        (res) => {
          let uniqueControlFrequencies = [];
          res.results.forEach(control => {
            if (!uniqueControlFrequencies.some(controlFrequency => controlFrequency.value === control.control_frequency_text[0])) {
              uniqueControlFrequencies.push({
                value: control.control_frequency_text[0],
                text: control.control_frequency_text[1]
              });
            }
          });
          setPeriodicity(uniqueControlFrequencies);
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
    return <div>{t('risks.loading-domain-risks')}...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            {periodicity.map((value, index) => {
              return <p key={value.value}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value.value)} className="form-check-input" name="process" type="checkbox" value={value.value} />
                  <span className="fw-semibold ps-2 fs-6">{value.text}</span>
                </label>
              </p>
            })}
          </>
        )}
      </div>
    );
  }
}

export default SelectPeriodicity;
