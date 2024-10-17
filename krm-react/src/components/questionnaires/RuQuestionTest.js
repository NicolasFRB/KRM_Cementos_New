import configService from "../../services/config.js";
import React from "react";
import { useState } from "react";
import { useTranslation } from "react-i18next";

let $ = window.$;

function RuQuestionTest({ pk, initialAnswer, initialDescription }) {
  const [answer, setAnswer] = useState(initialAnswer);
  const [description, setDescription] = useState(initialDescription);

  const [t] = useTranslation("global");

  const updateAnswer = (newAnswer) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendQuestionTest}?pk=${pk}&answer=${newAnswer}`)
      .then((res) => res.json())
      .then(
        (res) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        },
        (error) => {
          $('#buttonSend').attr('data-kt-indicator', 'off');
        }
      );
    setAnswer(newAnswer);

    if (newAnswer === 1) {
      $(`#id-description--${pk}`).focus();
      if (description === '') {
        $(`#id-description--${pk}`).addClass('is-invalid');
      }
    }
  };

  const updateDescription = (newDescription) => {
    $('#buttonSend').attr('data-kt-indicator', 'on');
    fetch(`${configService.apiSendQuestionTest}?pk=${pk}&description=${newDescription}`)
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
    if (newDescription !== '' && answer !== 2) {
      $(`#id-description--${pk}`).removeClass('is-invalid');
    } else {
      if (newDescription === '' && answer === 2) {
        $(`#id-description--${pk}`).addClass('is-invalid');
      }
    }
  };

  return (
    <div className="valoration">
      <div className="row">
        <div className="col col-12">

          <h4 className="mb-7 mt-5">{t('questions.complete-answer')}</h4>
        </div>
        <input type="hidden" name={`answer-${pk}`} value={answer} />

        <div className="row">
          <div className="col col-12 col-xl-10 mb-1 mb-xl-0">
            <div className="row">
              <div className="col col-12 col-md-4">
                <h5 className="mb-7">{t('questions.answer')}</h5>
                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`a-pk-1-${pk}`}
                    checked={answer === 1}
                    onChange={() => updateAnswer(1)}
                  />
                  <label className="form-check-label" htmlFor={`a-pk-1-${pk}`}>{t('questions.yes')}</label>
                </div>

                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`a-pk-2-${pk}`}
                    checked={answer === 2}
                    onChange={() => updateAnswer(2)}
                  />
                  <label className="form-check-label" htmlFor={`a-pk-2-${pk}`}>{t('questions.no')}</label>
                </div>

                <div className="form-check form-check-custom form-check-solid mb-4">
                  <input
                    name={`p-${pk}`}
                    className="form-check-input"
                    type="radio"
                    id={`a-pk-3-${pk}`}
                    checked={answer === 3}
                    onChange={() => updateAnswer(3)}
                  />
                  <label className="form-check-label" htmlFor={`a-pk-3-${pk}`}>{t('questions.n-a')}</label>
                </div>
              </div>

              <div className="col col-12 col-md-6">
                <div className="form-group">
                  <label htmlFor={`id-description--${pk}`} className=""><h5>{t('questions.comments')}</h5></label>
                  <textarea required cols="40" rows="4" name={`description-${pk}`} id={`id-description--${pk}`} className="form-control" onBlur={(e) => updateDescription(e.currentTarget.value)} value={description} onChange={(e) => setDescription(e.currentTarget.value)} placeholder={t('questions.no-comments')}></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div >
  );
}

export default RuQuestionTest;
