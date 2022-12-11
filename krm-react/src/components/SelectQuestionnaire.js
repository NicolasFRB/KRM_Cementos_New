import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import Select from 'react-select'
import { useTranslation } from "react-i18next";

function SelectQuestionnaire({ questionnaire, setQuestionnaire, selectedQuestions, setSelectedQuestions, scopes, setScopes }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);

  // const [questionnaires, setQuestionnaires] = useState([]);
  const [selectOptions, setSelectOptions] = useState([]);

  const [t] = useTranslation("global");

  useEffect(() => {
    fetch(configService.apiGetQuestionnaires)
      .then((res) => res.json())
      .then(
        (res) => {
          // setQuestionnaires(res.results);
          let newSelectOptions = res.results.map((questionnaire) => {
            return {
              value: questionnaire.pk,
              label: questionnaire.name,
              scopes: questionnaire.scopes_names,
            }
          });
          newSelectOptions.unshift({ value: 0, label: '-', scopes: [] });
          setSelectOptions(newSelectOptions);
          setIsLoaded(true);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, []);

  useEffect(() => {
    setScopes(null)
  }, [questionnaire, setScopes]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>{t('general.loading-questionnaires')}...</div>;
  } else {
    return (
      <div>
        {isLoaded && selectOptions && (
          <div className="row">
            <div className="col col-12 col-sm-6">
              <h5>Cuestionario</h5>
              <Select options={selectOptions} defaultValue={selectOptions[0]} onChange={setQuestionnaire} selectedQuestions={selectedQuestions} setSelectedQuestions={setSelectedQuestions} />
              <input type="hidden" name="questionnaire" value={questionnaire.value} />
            </div>
            {questionnaire.scopes && (
              <div className="col col-12 col-sm-6">
                <h5>Alcances</h5>
                <Select options={questionnaire.scopes} key={questionnaire.value} isMulti onChange={(scopes) => setScopes(scopes)} />
              </div>
            )}
          </div>
        )}
      </div>
    );
  }
}

export default SelectQuestionnaire;
