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

  const selectAll = () => {
    setSelectedRisks(risks.map(risk => {
      return risk.pk;
    }));
  };

  const unSelectAll = () => {
    setSelectedRisks([]);
  };

  useEffect(() => {
    fetch(`${configService.apiGetRisks}`)
      .then((res) => res.json())
      .then(
        (res) => {
          setRisks(res.results.map(risk => {
            return { ...risk, checked: false }
          }));
          setIsLoaded(true);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, []);

  useEffect(() => {
    if (risks.length) {
      window.CustomDatatables.initEvalRI();
    }
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
            <table className="table table-striped customDatatable" id="riskri">
              <thead>
                <tr>
                  <th className="text-center">
                    <span onClick={() => selectAll()} className="me-5"><i className="bi bi-clipboard-check"></i></span>
                    <span onClick={() => unSelectAll()}><i className="bi bi-clipboard"></i></span>
                  </th>
                  <th className="fw-semibold">REF</th>
                  <th className="fw-semibold">NOMBRE</th>
                  <th className="fw-semibold">RIESGO MAESTRO</th>
                </tr>
              </thead>
              <tbody>
                {risks.map((risk, index) => {
                  return <tr key={risk.pk}>
                    <td className="text-center">
                      <label className="form-check form-check-inline form-check-solid"><input id={'ri' + risk.pk} onChange={() => handleOnChange(risk.pk)} className="form-check-input" name="risks" type="checkbox" value={risk.pk} checked={selectedRisks.includes(risk.pk)} /></label>
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
