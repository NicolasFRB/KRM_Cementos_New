import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectPeriodicity({ selectedPeriodicity, setSelectedPeriodicity }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [periodicity, setPeriodicity] = useState([]);

  let url = configService.apiGetControlPeriodicity;
  if (window.location.pathname.includes("/en/")) {
    url = url.replace("/es/", "/en/");
  }

  const handleOnChange = (pk) => {
    if (selectedPeriodicity.includes(pk)) {
      setSelectedPeriodicity(selectedPeriodicity.filter(item => item !== pk));
    } else {
      setSelectedPeriodicity(selectedPeriodicity.concat([pk]));
    }
  };

  const [t] = useTranslation("global");

  // quiero saber si estoy viendo la página en español o en inglés

  useEffect(() => {
    fetch(`${url}`)
      .then((res) => res.json())
      .then(
        (res) => {
          console.log(res);
          let perio = [];
          res.forEach(choice => {
            perio.push({
              value: choice[0],
              text: choice[1]
            });
          });
          setPeriodicity(perio);
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
