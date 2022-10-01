import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";

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

  useEffect(() => {
    window.CustomDatatables.destroy();
    window.CustomDatatables.init();
  }, [risks]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>Cargando riesgos...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <table className="table table-striped customDatatable">
              <thead>
                <tr>
                  <th className="fw-semibold"></th>
                  <th className="fw-semibold">REF</th>
                  <th className="fw-semibold">NOMBRE</th>
                  <th className="fw-semibold">RIESGO MAESTRO</th>
                </tr>
              </thead>
              <tbody>
                {risks.map((risk, index) => {
                  return <tr key={risk.pk}>
                    <td className="text-center">
                      <label className="form-check form-check-inline form-check-solid"><input id={'ri' + risk.pk} onChange={() => handleOnChange(risk.pk)} className="form-check-input" name="risks" type="checkbox" value={risk.pk} /></label>
                    </td>
                    <td><label htmlFor={'ri' + risk.pk}>{risk.ref}</label></td>
                    <td><span className="fw-semibold">{risk.name}</span></td>
                    <td>{risk.risk_master_name}</td>
                  </tr>
                })}
              </tbody>
            </table>
          </>
        )}
      </div>
    );
  }
}

export default SelectRisk;
