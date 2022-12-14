import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

import SelectQuestionnaire from "./SelectQuestionnaire.js";
import SelectScopes from "./SelectScopes.js";
import SelectQuestions from "./SelectQuestions.js";

let $ = window.$;

function CreateEvaluationQuestionnaire(props) {
  const [formData, setFormData] = useState({ 'completed': false });
  const [questionnaire, setQuestionnaire] = useState({ value: 0, label: '-' });
  const [selectedQuestions, setSelectedQuestions] = useState([]);
  const [nQuestionTests, setNQuestionTests] = useState(0);
  const [scopes, setScopes] = useState([]);
  const [scopesSelected, setScopesSelected] = useState([]);
  const [questions, setQuestions] = useState([]);

  const readFormData = () => {
    let newFormData = {};
    newFormData.ref = $('#e_ref').val();
    newFormData.date_begin = $('#e_date_begin').val();
    newFormData.date_end = $('#e_date_end').val();
    newFormData.description = $('#e_description').val();
    newFormData.completed = newFormData.ref !== '' && newFormData.date_begin !== '' && newFormData.date_intermediate !== '' && newFormData.date_end !== '';
    setFormData(newFormData);
  }

  const [t] = useTranslation("global");

  useEffect(() => {
    $('#e_ref, #e_date_begin, #e_date_intermediate, #e_date_end, #e_description').on('change', readFormData);
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    let nQuestionTests = 0;
    selectedQuestions.forEach((question) => {
      nQuestionTests += question.evaluators.length;
    });
    setNQuestionTests(nQuestionTests);
  }, [selectedQuestions]);

  const sendForm = (e) => {
    e.preventDefault();
    if (formData.completed === false) {
      alert('Falta algún dato imprescindible en el formulario');
      return false;
    }

    $(e.currentTarget).attr('data-kt-indicator', 'on');
    document.getElementById("evaluation_questionnaire_create").submit();
  }

  return (
    <div className="App">
      <div className="row">
        <div className="col-12">
          <h3 className="mb-6">{t('q.step-2')}</h3>
          {formData.completed === false && (
            <div className="alert alert-primary">{t('q.complete-data')}</div>
          )}
          <div className={(formData.completed ? '' : 'd-none')}>
            <div className="row">
              <div className="col col-12 col-sm-6">
                <SelectQuestionnaire questionnaire={questionnaire} setQuestionnaire={setQuestionnaire} scopes={scopes} setScopes={setScopes} setScopesSelected={setScopesSelected} />
              </div>
              {questionnaire.value !== 0 && (
                <div className="col col-12 col-sm-6" key={questionnaire.value}>
                  <SelectScopes scopes={scopes} setScopesSelected={setScopesSelected} />
                </div>
              )}
            </div>
          </div>
          <div className="separator my-10"></div>
        </div>
        <div className="col-12">
          <h3 className="mb-5">{t('q.step-3')}</h3>
          {(questionnaire.value !== 0 && scopesSelected && scopesSelected.length > 0) ? (
            <SelectQuestions questionnaire={questionnaire} selectedQuestions={selectedQuestions} setSelectedQuestions={setSelectedQuestions} scopesSelected={scopesSelected} questions={questions} setQuestions={setQuestions} scopes={scopes} />
          ) : (
            <div className="alert alert-primary">{t('q.select-questionnaire')}</div>
          )}
        </div>

        <div className="separator my-10"></div>
        <div className="col-12" id="launch">
          <h3 className="mb-5">{t('q.step-4')}</h3>
          {selectedQuestions.length === 0 ? (
            <div className="alert alert-primary">{t('q.select-question')}</div>
          ) : (
            <div className="col-12">
              <p>{t('q.questions-to-launch', { 'nquestions': nQuestionTests })} </p>
              <button onClick={sendForm} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap" data-kt-indicator="off">
                <span className="indicator-label">{t('q.launch')}</span>
                <span className="indicator-progress">
                  {t('q.launching')}...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                </span>
              </button>
              <input type="hidden" name="questions_to_evaluate" value={JSON.stringify(selectedQuestions.map((question) => {
                return {
                  pk: question.pk,
                  scope: question.scope,
                  evaluators: question.evaluators.map((evaluator) => {
                    return evaluator.value
                  })
                };
              }))} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CreateEvaluationQuestionnaire;
