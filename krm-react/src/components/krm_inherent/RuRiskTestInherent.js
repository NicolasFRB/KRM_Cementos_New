import configService from "../../services/config.js";
import React from "react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

let $ = window.$;

function RuRiskTestInherent({ pk, initialImpactReputational, initialImpactEconomic, initialImpactRegulatory, initialImpactObjectives, initialImpactDedication, initialProbability, initialEventSpeed, initialDescription }) {
  const [impactReputational, setImpactReputational] = useState(initialImpactReputational);
  const [impactEconomic, setImpactEconomic] = useState(initialImpactEconomic);
  const [impactRegulatory, setImpactRegulatory] = useState(initialImpactRegulatory);
  const [impactObjectives, setImpactObjectives] = useState(initialImpactObjectives);
  const [impactDedication, setImpactDedication] = useState(initialImpactDedication);
  const [probability, setProbability] = useState(initialProbability);
  const [eventSpeed, setEventSpeed] = useState(initialEventSpeed);
  const [description, setDescription] = useState(initialDescription);

  const [t] = useTranslation("global");

  const updateProbability = (newProbability) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&probability=${newProbability}`)
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

  const updateImpactReputational = (newImpactReputational) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactReputational=${newImpactReputational}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactReputational(newImpactReputational);
  };

  const updateImpactEconomic = (newImpactEconomic) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactEconomic=${newImpactEconomic}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactEconomic(newImpactEconomic);
  };

  const updateImpactRegulatory = (newImpactRegulatory) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactRegulatory=${newImpactRegulatory}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactRegulatory(newImpactRegulatory);
  };

  const updateImpactObjectives = (newImpactObjectives) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactObjectives=${newImpactObjectives}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactObjectives(newImpactObjectives);
  };

  const updateImpactDedication = (newImpactDedication) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactDedication=${newImpactDedication}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactDedication(newImpactDedication);
  };

  const updateEventSpeed = (newEventSpeed) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&eventSpeed=${newEventSpeed}`)
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

  const updateDescription = (newDescription) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&description=${newDescription}`)
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
          <h4 className="mb-7">{t('krmInherent.set-value')}</h4>
        </div>
        <input type="hidden" name={`probability-${pk}`} value={probability} />
        <input type="hidden" name={`impact-reputational-${pk}`} value={impactReputational} />
        <input type="hidden" name={`impact-economic-${pk}`} value={impactEconomic} />
        <input type="hidden" name={`impact-regulatory-${pk}`} value={impactRegulatory} />
        <input type="hidden" name={`impact-objectives-${pk}`} value={impactObjectives} />
        <input type="hidden" name={`impact-dedication-${pk}`} value={impactDedication} />
        <input type="hidden" name={`event-speed-${pk}`} value={eventSpeed} />

        <div className="row mb-10">
          <div className="col col-12 col-xl-5 mb-5 mb-xl-0">
            <h5 className="mb-7">{t('krmInherent.probability')}</h5>
            <div className= "row">

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
          </div>

          <div className="col col-12 col-xl-5 offset-xl-1">
            <h5 className="mb-7">{t('krmInherent.impact-reputational')}</h5>
            <div className= "row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-reputational-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-reputational-1-${pk}`}
                    checked={impactReputational === 1}
                    onChange={() => updateImpactReputational(1)}
                  />
                  <label className="form-check-label" htmlFor={`impact-reputational-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-reputational-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-reputational-2-${pk}`}
                    checked={impactReputational === 2}
                    onChange={() => updateImpactReputational(2)}
                  />
                  <label className="form-check-label" htmlFor={`impact-reputational-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-reputational-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-reputational-3-${pk}`}
                    checked={impactReputational === 3}
                    onChange={() => updateImpactReputational(3)}
                  />
                  <label className="form-check-label" htmlFor={`impact-reputational-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-reputational-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-reputational-4-${pk}`}
                    checked={impactReputational === 4}
                    onChange={() => updateImpactReputational(4)}
                  />
                  <label className="form-check-label" htmlFor={`impact-reputational-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-reputational-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-reputational-5-${pk}`}
                    checked={impactReputational === 5}
                    onChange={() => updateImpactReputational(5)}
                  />
                  <label className="form-check-label" htmlFor={`impact-reputational-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div className="row mb-10">
          <div className="col col-12 col-xl-5">
            <h5 className="mb-7">{t('krmInherent.impact-economic')}</h5>
            <div className= "row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-pk-economic-1-${pk}`}
                    checked={impactEconomic === 1}
                    onChange={() => updateImpactEconomic(1)}
                  />
                  <label className="form-check-label" htmlFor={`impact-pk-economic-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-pk-economic-2-${pk}`}
                    checked={impactEconomic === 2}
                    onChange={() => updateImpactEconomic(2)}
                  />
                  <label className="form-check-label" htmlFor={`impact-pk-economic-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-pk-economic-3-${pk}`}
                    checked={impactEconomic === 3}
                    onChange={() => updateImpactEconomic(3)}
                  />
                  <label className="form-check-label" htmlFor={`impact-pk-economic-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-pk-economic-4-${pk}`}
                    checked={impactEconomic === 4}
                    onChange={() => updateImpactEconomic(4)}
                  />
                  <label className="form-check-label" htmlFor={`impact-pk-economic-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-pk-economic-5-${pk}`}
                    checked={impactEconomic === 5}
                    onChange={() => updateImpactEconomic(5)}
                  />
                  <label className="form-check-label" htmlFor={`impact-economic-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>

          <div className="col col-12 col-xl-5 offset-xl-1">
            <h5 className="mb-7">{t('krmInherent.impact-regulatory')}</h5>
            <div className= "row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-regulatory-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-regulatory-1-${pk}`}
                    checked={impactRegulatory === 1}
                    onChange={() => updateImpactRegulatory(1)}
                  />
                  <label className="form-check-label" htmlFor={`impact-regulatory-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-regulatory-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-regulatory-2-${pk}`}
                    checked={impactRegulatory === 2}
                    onChange={() => updateImpactRegulatory(2)}
                  />
                  <label className="form-check-label" htmlFor={`impact-regulatory-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-regulatory-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-regulatory-3-${pk}`}
                    checked={impactRegulatory === 3}
                    onChange={() => updateImpactRegulatory(3)}
                  />
                  <label className="form-check-label" htmlFor={`impact-regulatory-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-regulatory-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-regulatory-4-${pk}`}
                    checked={impactRegulatory === 4}
                    onChange={() => updateImpactRegulatory(4)}
                  />
                  <label className="form-check-label" htmlFor={`impact-regulatory-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-regulatory-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-regulatory-5-${pk}`}
                    checked={impactRegulatory === 5}
                    onChange={() => updateImpactRegulatory(5)}
                  />
                  <label className="form-check-label" htmlFor={`impact-regulatory-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div className= "row mb-10">
          <div className="col col-12 col-xl-5">
            <h5 className="mb-7">{t('krmInherent.impact-objectives')}</h5>
            <div className= "row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-objectives-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-objectives-1-${pk}`}
                    checked={impactObjectives === 1}
                    onChange={() => updateImpactObjectives(1)}
                  />
                  <label className="form-check-label" htmlFor={`impact-objectives-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-objectives-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-objectives-2-${pk}`}
                    checked={impactObjectives === 2}
                    onChange={() => updateImpactObjectives(2)}
                  />
                  <label className="form-check-label" htmlFor={`impact-objectives-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-objectives-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-objectives-3-${pk}`}
                    checked={impactObjectives === 3}
                    onChange={() => updateImpactObjectives(3)}
                  />
                  <label className="form-check-label" htmlFor={`impact-objectives-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-objectives-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-objectives-4-${pk}`}
                    checked={impactObjectives === 4}
                    onChange={() => updateImpactObjectives(4)}
                  />
                  <label className="form-check-label" htmlFor={`impact-objectives-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-objectives-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-objectives-5-${pk}`}
                    checked={impactObjectives === 5}
                    onChange={() => updateImpactObjectives(5)}
                  />
                  <label className="form-check-label" htmlFor={`impact-objectives-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>

          <div className="col col-12 col-xl-5 offset-xl-1">
            <h5 className="mb-7">{t('krmInherent.impact-dedication')}</h5>
            <div className= "row">
              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-dedication-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-dedication-1-${pk}`}
                    checked={impactDedication=== 1}
                    onChange={() => updateImpactDedication(1)}
                  />
                  <label className="form-check-label" htmlFor={`impact-dedication-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-dedication-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-dedication-2-${pk}`}
                    checked={impactDedication === 2}
                    onChange={() => updateImpactDedication(2)}
                  />
                  <label className="form-check-label" htmlFor={`impact-dedication-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-dedication-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-dedication-3-${pk}`}
                    checked={impactDedication === 3}
                    onChange={() => updateImpactDedication(3)}
                  />
                  <label className="form-check-label" htmlFor={`impact-dedication-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-dedication-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-dedication-4-${pk}`}
                    checked={impactDedication === 4}
                    onChange={() => updateImpactDedication(4)}
                  />
                  <label className="form-check-label" htmlFor={`impact-dedication-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`impact-dedication-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`impact-dedication-5-${pk}`}
                    checked={impactDedication === 5}
                    onChange={() => updateImpactDedication(5)}
                  />
                  <label className="form-check-label" htmlFor={`impact-dedication-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div className= "row mb-10">
          <div className="col col-12 col-xl-5">
            <h5 className="mb-7">{t('krmInherent.event-speed')}</h5>
            <div className= "row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-1-${pk}`}
                    checked={eventSpeed === 1}
                    onChange={() => updateEventSpeed(1)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-1-${pk}`}>{t('krmInherent.very-low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-2-${pk}`}
                    checked={eventSpeed === 2}
                    onChange={() => updateEventSpeed(2)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-2-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-3-${pk}`}
                    checked={eventSpeed === 3}
                    onChange={() => updateEventSpeed(3)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-3-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-4-${pk}`}
                    checked={eventSpeed === 4}
                    onChange={() => updateEventSpeed(4)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-4-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`event-speed-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`event-speed-5-${pk}`}
                    checked={eventSpeed === 5}
                    onChange={() => updateEventSpeed(5)}
                  />
                  <label className="form-check-label" htmlFor={`event-speed-5-${pk}`}>{t('krmInherent.very-high')}</label>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>

      <div className="row">
        <div className="form-group">
          <label htmlFor={`id-description--${pk}`} className=""><h5>{t('krmInherent.description-value-expert')} (*)</h5></label>
          <textarea required cols="40" rows="3" name={`description-${pk}`} id={`id-description--${pk}`} className="form-control" onBlur={(e) => updateDescription(e.currentTarget.value)} value={description} onChange={(e) => setDescription(e.currentTarget.value)}></textarea>
        </div>
      </div>
    </div >
  );
}

export default RuRiskTestInherent;
