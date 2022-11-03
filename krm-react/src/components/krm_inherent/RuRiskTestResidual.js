import configService from "../../services/config.js";
import React from "react";
import { useState } from "react";

let $ = window.$;

function RuRiskTestResidual({ pk, initialProbability, initialDescription }) {
  const [probability, setProbability] = useState(initialProbability);
  const [description, setDescription] = useState(initialDescription);

  const updateProbability = (newProbability) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestResidual}?pk=${pk}&probability=${newProbability}`)
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

  const updateDescription = (newDescription) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestResidual}?pk=${pk}&description=${newDescription}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setDescription(newDescription);
  };

  return (
    <div className="valoration">
      <div className="row">
        <div className="col col-12">
          <h4 className="mb-7">Indique su valoración como Evaluador del Dominio de Riesgo Residual</h4>
        </div>
        <input type="hidden" name={`probability-${pk}`} value={probability} />

        <div className="row mb-10">
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
            <label htmlFor={`id-description--${pk}`} className=""><h5>Descripción de la valoración del evaluador de Dominio de Riesgo (*)</h5></label>
            <textarea required cols="40" rows="3" name={`description-${pk}`} id={`id-description--${pk}`} className="form-control" onBlur={(e) => updateDescription(e.currentTarget.value)} value={description} onChange={(e) => setDescription(e.currentTarget.value)}></textarea>
          </div>
        </div>
      </div>
    </div >
  );
}

export default RuRiskTestResidual;