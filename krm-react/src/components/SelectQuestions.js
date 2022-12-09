import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import Select from 'react-select'
import { useTranslation } from "react-i18next";

function SelectQuestions(
  {
    questionnaire,
    selectedQuestions,
    setSelectedQuestions
  }) {
  const [error, setError] = useState(null);
  const [questionsIsLoaded, setQuestionsIsLoaded] = useState(false);
  const [usersIsLoaded, setUsersIsLoaded] = useState(false);
  const [selectOptions, setSelectOptions] = useState([]);
  const [questions, setQuestions] = useState([]);

  const [t] = useTranslation("global");

  const handleEvaluators = (evaluators, q) => {
    let newQuestions = questions.map((question) => {
      if (question.pk === q.pk) {
        if (Array.isArray(evaluators)) {
          question.evaluators = evaluators;
          if (evaluators.length === 0) {
            setSelectedQuestions(selectedQuestions.filter(question => question.pk !== q.pk));
          }
        } else {
          question.evaluators = [];
          setSelectedQuestions(selectedQuestions.filter(question => question.pk !== q.pk));
        }
      }
      return question;
    });
    setQuestions(newQuestions);

    if (evaluators.length) {
      let newSelectedQuestions = selectedQuestions.map((question) => {
        if (question.pk === q.pk) {
          question.evaluators = evaluators;
        }
        return question;
      });
      setSelectedQuestions(newSelectedQuestions);
    } else {
      setSelectedQuestions(selectedQuestions.filter(question => question.pk !== q.pk));
    }
  };

  const handleOnChange = (question) => {
    if (selectedQuestions.find(q => q.pk === question.pk)) {
      setSelectedQuestions(selectedQuestions.filter(q => q.pk !== question.pk));
    } else {
      setSelectedQuestions(selectedQuestions.concat([question]));
    }
  };

  const selectAll = () => {
    setSelectedQuestions(questions.filter(question => question.evaluators.length > 0));
  };

  const unSelectAll = () => {
    setSelectedQuestions([]);
  };

  useEffect(() => {
    fetch(configService.apiGetUsers)
      .then((res) => res.json())
      .then(
        (res) => {
          let newSelectOptions = res.results.map((user) => {
            return {
              value: user.pk,
              label: user.email
            }
          });
          setSelectOptions(newSelectOptions);
          setUsersIsLoaded(true);
        },
        (error) => {
          setUsersIsLoaded(true);
          setError(error);
        }
      );
  }, []);

  useEffect(() => {
    setQuestionsIsLoaded(false);
    const params = {
      questionnaire: questionnaire.value,
    };
    var url = new URL(`${configService.apiGetQuestions}`);
    for (let k in params) {
      url.searchParams.append(k, params[k]);
    }
    fetch(url)
      .then((res) => res.json())
      .then(
        (res) => {
          setQuestions(res.results.map((question) => {
            let evaluators = question.user_to_assign_emails.map((question) => { return question.value });
            return {
              ...question,
              evaluators: question.user_to_assign_emails,
            }
          }));
          setQuestionsIsLoaded(true);
        },
        (error) => {
          setQuestionsIsLoaded(true);
          setError(error);
        }
      );
  }, [questionnaire]);

  useEffect(() => {
    setSelectedQuestions([]);
  }, [questionnaire, setSelectedQuestions]);


  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!questionsIsLoaded || !usersIsLoaded) {
    return <div>{t('questions.loading-questions')}...</div>;
  } else {
    return (
      <div>
        {questionsIsLoaded && usersIsLoaded && (
          <div className="col col-12">
            <h5>{t('questions.questions-to-evaluate')}</h5>
            <p>{t('questions.assign-evaluators')}</p>
            <table className="table table-striped customDatatable">
              <thead>
                <tr>
                  <th className="text-center">
                    <span onClick={() => selectAll()} className="me-5"><i className="bi bi-clipboard-check"></i></span>
                    <span onClick={() => unSelectAll()}><i className="bi bi-clipboard"></i></span>
                  </th>
                  <th className="fw-semibold">REF</th>
                  <th className="fw-semibold">{t('general.title')}</th>
                  <th className="fw-semibold text-center">{t('general.evaluators')}</th>
                </tr>
              </thead>
              <tbody>
                {questions.map((question, index) => {
                  return <tr key={question.pk}>
                    <td className="text-center" width="100px">
                      {question.evaluators.length === 0 ? (
                        <span className="badge badge-square badge-danger" data-bs-toggle="tooltip" data-bs-placement="top" title={t('questions.no-posible')}></span>
                      ) : (
                        <input name="qs" value={question.pk} onChange={() => handleOnChange(question)} className="form-check-input" type="checkbox" checked={selectedQuestions.find(q => q.pk === question.pk) !== undefined} />
                      )}
                    </td>
                    <td>{question.ref}</td>
                    <td>{question.title}</td>
                    <td width="40%">
                      {usersIsLoaded && (
                        <Select options={selectOptions} isMulti onChange={(evaluators) => handleEvaluators(evaluators, question)} defaultValue={question.user_to_assign_emails} />
                      )}
                    </td>
                  </tr>
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    );
  }
}

export default SelectQuestions;
