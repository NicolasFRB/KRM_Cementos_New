import configService from "../../services/config.js";
import React from "react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

let $ = window.$;

function RuRiskTestInherent({ pk, initialImpactEconomic, initialImpactContinuity, initialImpactBranding, initialProbability, initialDescription }) {
  const [impactEconomic, setImpactEconomic] = useState(initialImpactEconomic);
  const [impactContinuity, setImpactContinuity] = useState(initialImpactContinuity);
  const [impactBranding, setImpactBranding] = useState(initialImpactBranding);
  const [probability, setProbability] = useState(initialProbability);
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

  const updateImpactContinuity = (newImpactContinuity) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactContinuity=${newImpactContinuity}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactContinuity(newImpactContinuity);
  };

  const updateImpactBranding = (newImpactBranding) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendRiskTestInherent}?pk=${pk}&impactBranding=${newImpactBranding}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setImpactBranding(newImpactBranding);
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
        <input type="hidden" name={`impact-continuity-${pk}`} value={impactContinuity} />
        <input type="hidden" name={`impact-economic-${pk}`} value={impactEconomic} />
        <input type="hidden" name={`impact-branding-${pk}`} value={impactBranding} />

        <div className="row mb-10">
          <div className="col col-12 col-xl-5 mb-5 mb-xl-0">
            <h5 className="mb-7">{t('krmInherent.probability')}</h5>
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
                  <label className="form-check-label" htmlFor={`p-pk-1-${pk}`}>{t('krmInherent.low')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-2-${pk}`}>{t('krmInherent.medium')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-3-${pk}`}>{t('krmInherent.high')}</label>
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
                  <label className="form-check-label" htmlFor={`p-pk-4-${pk}`}>{t('krmInherent.critic')}</label>
                </div>
              </div>

            </div>
          </div>

          <div className="col col-12 col-xl-5 offset-xl-1">
            <h5 className="mb-7">{t('krmInherent.impact-continuity')}</h5>
            <div className="row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-continuity-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-1-${pk}`}
                    checked={impactContinuity === 1}
                    onChange={() => updateImpactContinuity(1)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-1-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-continuity-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-2-${pk}`}
                    checked={impactContinuity === 2}
                    onChange={() => updateImpactContinuity(2)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-2-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-continuity-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-3-${pk}`}
                    checked={impactContinuity === 3}
                    onChange={() => updateImpactContinuity(3)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-3-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-continuity-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-4-${pk}`}
                    checked={impactContinuity === 4}
                    onChange={() => updateImpactContinuity(4)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-4-${pk}`}>{t('krmInherent.critic')}</label>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div className="row mb-10">
          <div className="col col-12 col-xl-5">
            <h5 className="mb-7">{t('krmInherent.impact-economic')}</h5>
            <div className="row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-economic-1-${pk}`}
                    checked={impactEconomic === 1}
                    onChange={() => updateImpactEconomic(1)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-economic-1-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-economic-2-${pk}`}
                    checked={impactEconomic === 2}
                    onChange={() => updateImpactEconomic(2)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-economic-2-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-economic-3-${pk}`}
                    checked={impactEconomic === 3}
                    onChange={() => updateImpactEconomic(3)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-economic-3-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-economic-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-economic-4-${pk}`}
                    checked={impactEconomic === 4}
                    onChange={() => updateImpactEconomic(4)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-economic-4-${pk}`}>{t('krmInherent.critic')}</label>
                </div>
              </div>

            </div>
          </div>

          <div className="col col-12 col-xl-5 offset-xl-1">
            <h5 className="mb-7">{t('krmInherent.impact-branding')}</h5>
            <div className="row">

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-branding-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-branding-1-${pk}`}
                    checked={impactBranding === 1}
                    onChange={() => updateImpactBranding(1)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-branding-1-${pk}`}>{t('krmInherent.low')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-branding-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-branding-2-${pk}`}
                    checked={impactBranding === 2}
                    onChange={() => updateImpactBranding(2)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-branding-2-${pk}`}>{t('krmInherent.medium')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-branding-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-branding-3-${pk}`}
                    checked={impactBranding === 3}
                    onChange={() => updateImpactBranding(3)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-branding-3-${pk}`}>{t('krmInherent.high')}</label>
                </div>
              </div>

              <div className="col">
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`ì-branding-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`i-pk-branding-4-${pk}`}
                    checked={impactBranding === 4}
                    onChange={() => updateImpactBranding(4)}
                  />
                  <label className="form-check-label" htmlFor={`i-pk-branding-4-${pk}`}>{t('krmInherent.critic')}</label>
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
      </div>
    </div >
  );
}

export default RuRiskTestInherent;
