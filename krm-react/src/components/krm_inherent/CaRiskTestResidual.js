import configService from "../../services/config.js";
import React from "react";
import { useState } from "react";

let $ = window.$;

function CaRiskTestResidual({ pk, initialProbability, initialDescriptionAdmin }) {
  const [probability, setProbability] = useState(initialProbability);
  const [descriptionAdmin, setDescriptionAdmin] = useState(initialDescriptionAdmin);

  const updateProbability = (newProbability) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskCompanyResidualAdmin}?pk=${pk}&adminProbability=${newProbability}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setProbability(newProbability);
  };

  const updateDescriptionAdmin = (newDescriptionAdmin) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskCompanyResidualAdmin}?pk=${pk}&descriptionAdmin=${newDescriptionAdmin}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setDescriptionAdmin(newDescriptionAdmin);
  };


  return (
    <div className="valoration">
      <div className="row">
        <div className="col col-12">
          <h4 className="mb-7">Nivel de Control Administrador de la compañía evaluada</h4>
        </div>
        <input type="hidden" name={`probability-${pk}`} value={probability} />
        <div className="row mb-5">
          <div className="col col-12 col-xl-8 mb-5 mb-xl-0">
            <h5 className="mb-7">Nivel de Control</h5>
            <div className="row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`p-pk-1-${pk}`}
                    checked={probability === 1}
                    onChange={() => updateProbability(1)}
                  />
                  <label className="form-check-label" htmlFor={`p-pk-1-${pk}`}>1 Optimizado</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`p-pk-2-${pk}`}
                    checked={probability === 2}
                    onChange={() => updateProbability(2)}
                  />
                  <label className="form-check-label" htmlFor={`p-pk-2-${pk}`}>2 Aceptable</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`p-pk-3-${pk}`}
                    checked={probability === 3}
                    onChange={() => updateProbability(3)}
                  />
                  <label className="form-check-label" htmlFor={`p-pk-3-${pk}`}>3 Inadecuado</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`p-pk-4-${pk}`}
                    checked={probability === 4}
                    onChange={() => updateProbability(4)}
                  />
                  <label className="form-check-label" htmlFor={`p-pk-4-${pk}`}>4 No controlado</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`p-pk-5-${pk}`}
                    checked={probability === 5}
                    onChange={() => updateProbability(5)}
                  />
                  <label className="form-check-label" htmlFor={`p-pk-4-${pk}`}>5 N/A</label>
                </div>
              </div>

            </div>
          </div>
        </div>
        <div className="row">
          <div className="form-group">
            <label htmlFor={`id-descriptionAdmin--${pk}`} className=""><h5>Descripción de la valoración del Administrador de la compañía evaluada (*)</h5></label>
            <textarea required cols="40" rows="3" name={`descriptionAdmin-${pk}`} id={`id-descriptionAdmin--${pk}`} className="form-control" onBlur={(e) => updateDescriptionAdmin(e.currentTarget.value)} value={descriptionAdmin} onChange={(e) => setDescriptionAdmin(e.currentTarget.value)}></textarea>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CaRiskTestResidual;