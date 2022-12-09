import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectRisk({ selectedRisks, setSelectedRisks }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [risks, setRisks] = useState([]);

  const handleOnChange = (pk) => {
    if (selectedRisks.includes(pk)) {
      setSelectedRisks(selectedRisks.filter(item => item !== pk));
    } else {
      setSelectedRisks(selectedRisks.concat([pk]));
    }
  };

  const [t] = useTranslation("global");

  useEffect(() => {
    fetch(`${configService.apiGetRisks}`)
      .then((res) => res.json())
      .then(
        (res) => {
          setRisks(res.results);
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
    return <div>{t('general.loading-risks')}...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <h5 className="mb-6">{t('general.select-risk')}</h5>
            {risks.map((value, index) => {
              return <p key={value.pk}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value.pk)} className="form-check-input" name="risks" type="checkbox" value={value.pk} />
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

export default SelectRisk;
