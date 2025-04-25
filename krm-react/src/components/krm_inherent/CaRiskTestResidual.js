import configService from "../../services/config.js";
import React from "react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

let $ = window.$;

function CaRiskTestResidual({ pk, initialImpact, initialProbability, initialEventSpeed, initialDescriptionAdmin }) {
  const [impact, setImpact] = useState(initialImpact);
  const [probability, setProbability] = useState(initialProbability);
  const [eventSpeed, setEventSpeed] = useState(initialEventSpeed);
  const [descriptionAdmin, setDescriptionAdmin] = useState(initialDescriptionAdmin);

  const [t] = useTranslation("global");

  const updateProbability = (newProbability) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestResidual}?pk=${pk}&adminProbability=${newProbability}`)
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

  const updateImpact = (newImpact) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestResidual}?pk=${pk}&adminImpact=${newImpact}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpact(newImpact);
  };

  const updateEventSpeed = (newEventSpeed) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestResidual}?pk=${pk}&adminEventSpeed=${newEventSpeed}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setEventSpeed(newEventSpeed);
  };

  const updateDescriptionAdmin = (newDescriptionAdmin) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestResidual}?pk=${pk}&descriptionAdmin=${newDescriptionAdmin}`)
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
          <h4 className="mb-7">{t('krmInherent.set-value-admin')}</h4>
        </div>
        <input type="hidden" name={`probability-${pk}`} value={probability} />
        <input type="hidden" name={`impact-${pk}`} value={impact} />
        <input type="hidden" name={`event-speed-${pk}`} value={eventSpeed} />

        <div className="row mb-5">
          <div className="col col-12 col-xl-5 mb-5 mb-xl-0">
            <h5 className="mb-7">{t('krmInherent.probability')}</h5>
            <div className="d-flex flex-nowrap justify-content-between">

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
                  <label className="form-check-label" htmlFor={`p-pk-1-${pk}`}>{t('krmInherent.remote')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-2-${pk}`}>{t('krmInherent.possible')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-3-${pk}`}>{t('krmInherent.probable')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-4-${pk}`}>{t('krmInherent.very-probable')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-5-${pk}`}>{t('krmInherent.certain')}</label>
                </div>
              </div>

            </div>

            <h5 className="mb-7">{t('krmInherent.event-speed')}</h5>
            <div className="d-flex flex-nowrap justify-content-between">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-pk-1-${pk}`}
                    checked={eventSpeed === 1}
                    onChange={() => updateEventSpeed(1)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-pk-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-pk-2-${pk}`}
                    checked={eventSpeed === 2}
                    onChange={() => updateEventSpeed(2)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-pk-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-pk-3-${pk}`}
                    checked={eventSpeed === 3}
                    onChange={() => updateEventSpeed(3)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-pk-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-pk-4-${pk}`}
                    checked={eventSpeed === 4}
                    onChange={() => updateEventSpeed(4)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-pk-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-pk-5-${pk}`}
                    checked={eventSpeed === 5}
                    onChange={() => updateEventSpeed(5)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-pk-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>
            </div>

          </div>

          <div className="col col-12 col-xl-5 offset-xl-1">
            <h5 className="mb-7">{t('krmInherent.impact')}</h5>
            <div className="d-flex flex-nowrap justify-content-between">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-1-${pk}`}
                    checked={impact === 1}
                    onChange={() => updateImpact(1)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-2-${pk}`}
                    checked={impact === 2}
                    onChange={() => updateImpact(2)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-3-${pk}`}
                    checked={impact === 3}
                    onChange={() => updateImpact(3)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-4-${pk}`}
                    checked={impact === 4}
                    onChange={() => updateImpact(4)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-5-${pk}`}
                    checked={impact === 5}
                    onChange={() => updateImpact(5)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>
        </div>
        <div className="row">
          <div className="form-group">
            <label htmlFor={`id-descriptionAdmin--${pk}`} className=""><h5>{t('krmInherent.description-value-admin')} (*)</h5></label>
            <textarea required cols="40" rows="3" name={`descriptionAdmin-${pk}`} id={`id-descriptionAdmin--${pk}`} className="form-control" onBlur={(e) => updateDescriptionAdmin(e.currentTarget.value)} value={descriptionAdmin} onChange={(e) => setDescriptionAdmin(e.currentTarget.value)}></textarea>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CaRiskTestResidual;
