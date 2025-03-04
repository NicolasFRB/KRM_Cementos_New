import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectScope({ selectedScopes, setSelectedScopes }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [scopes, setScopes] = useState([]);

  const handleOnChange = (value) => {
    if (selectedScopes.includes(value)) {
      setSelectedScopes(selectedScopes.filter(item => item !== value));
    } else {
      setSelectedScopes(selectedScopes.concat([value]));
    }
  };

  const [t] = useTranslation("global");

  useEffect(() => {
    fetch(`${configService.apiGetScopes}`)
      .then((res) => res.json())
      .then(
        (res) => {
          console.log("Scopes: ", res)
          setScopes(res);
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
            <h5 className="mb-6">{t('general.loading-scope')}</h5>
            {scopes.map((value, index) => {
              return <p key={value}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value)} className="form-check-input" name="scope" type="checkbox" value={value} />
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

export default SelectScope;
