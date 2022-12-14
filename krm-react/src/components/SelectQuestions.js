import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import Select from 'react-select'
import { useTranslation } from "react-i18next";
import { v4 as uuidv4 } from 'uuid';

function SelectQuestions(
  {
    questionnaire,
    selectedQuestions,
    setSelectedQuestions,
    scopesSelected,
    questions,
    setQuestions,
    scopes
  }) {
  const [error, setError] = useState(null);
  const [questionsIsLoaded, setQuestionsIsLoaded] = useState(false);
  const [usersIsLoaded, setUsersIsLoaded] = useState(false);
  const [selectOptions, setSelectOptions] = useState([]);
  const [filterQuestions, setFilterQuestions] = useState([]);

  const [t] = useTranslation("global");

  const getPosibleEvaluators = (scope) => {
    let scopeSelected = scopes.find(s => s.value === scope.scope_pk);
    let evaluators = [];
    if (scopeSelected) {
      evaluators = scopeSelected.posible_users.map((user) => {
        return {
          value: user.value,
          label: user.label
        }
      });
    }
    return evaluators;
  }

  const handleEvaluators = (evaluators, q) => {
    // degugger;
    let newQuestions = filterQuestions.map((question) => {
      if (question.uuid === q.uuid) {
        if (Array.isArray(evaluators)) {
          question.evaluators = evaluators;
          if (evaluators.length === 0) {
            setSelectedQuestions(selectedQuestions.filter(question => question.uuid !== q.uuid));
          }
        } else {
          question.evaluators = [];
          setSelectedQuestions(selectedQuestions.filter(question => question.uuid !== q.uuid));
        }
      }
      return question;
    });
    setFilterQuestions(newQuestions);

    if (evaluators.length) {
      let newSelectedQuestions = selectedQuestions.map((question) => {
        if (question.uuid === q.uuid) {
          question.evaluators = evaluators;
        }
        return question;
      });
      setSelectedQuestions(newSelectedQuestions);
    } else {
      setSelectedQuestions(selectedQuestions.filter(question => question.uuid !== q.uuid));
    }
  };

  const handleOnChange = (question) => {
    if (selectedQuestions.find(q => q.uuid === question.uuid)) {
      setSelectedQuestions(selectedQuestions.filter(q => q.uuid !== question.uuid));
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

  // useEffect(() => {
  //   window.CustomDatatables.destroy();
  //   window.CustomDatatables.init();
  // }, [filterQuestions]);

  // Nos traemos a los usuarios
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

  const checkQuestionInScopes = (question) => {
    if (scopesSelected.length === 0) {
      return true;
    }
    let encontrado = false;
    scopesSelected.forEach((scope) => {
      // console.log(question.ref + ": Check if " + question.scopes_names + " includes " + scope.label + ': ' + question.scopes_names.includes(scope.label));
      if (question.scopes_names.includes(scope.label)) {
        encontrado = true;
      }
    });
    return encontrado;
  }

  useEffect(() => {
    if (scopesSelected.length > 0 && questions.length > 0) {
      let newFilterQuestions = questions.filter(checkQuestionInScopes);
      let questionTests = [];
      newFilterQuestions.forEach((question) => {
        question.scopes.forEach((scope) => {
          if (scopesSelected.find(x => x.value === scope.scope_pk)) {
            questionTests.push({
              ...question,
              uuid: uuidv4(),
              scope: scope,
              evaluators: getPosibleEvaluators(scope),
              posible_evaluators: []
            });
          }
        });
      });
      // debugger;
      setFilterQuestions(questionTests);
      setQuestionsIsLoaded(true);
    }
    // eslint-disable-next-line
  }, [scopesSelected, questions]);

  useEffect(() => {
    setQuestionsIsLoaded(false);
    const params = {
      scopes__questionnaire: questionnaire.value,
    };
    var url = new URL(`${configService.apiGetQuestions}`);
    for (let k in params) {
      url.searchParams.append(k, params[k]);
    }
    fetch(url)
      .then((res) => res.json())
      .then(
        (res) => {
          setQuestions(res.results);
          // setQuestions(res.results.map((question) => {
          //   // let evaluators = question.potential_users_to_assign.map((question) => { return question.value });
          //   return question;
          //   // return {
          //   //   ...question,
          //   //   evaluators: question.potential_users_to_assign,
          //   // }
          // }));
          // setFilterQuestions(questions);
          // setQuestionsIsLoaded(true);
        },
        (error) => {
          setQuestionsIsLoaded(true);
          setError(error);
        }
      );
    // eslint-disable-next-line
  }, [questionnaire]);

  useEffect(() => {
    setSelectedQuestions([]);
  }, [questionnaire, setSelectedQuestions]);

  // useEffect(() => {
  //   window.CustomDatatables.destroy();
  //   window.CustomDatatables.init();
  // }, [scopes]);

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
                  <th className="text-center" width="100px">
                    <span onClick={() => selectAll()} className="me-5"><i className="bi bi-clipboard-check"></i></span>
                    <span onClick={() => unSelectAll()}><i className="bi bi-clipboard"></i></span>
                  </th>
                  <th className="fw-semibold">REF</th>
                  <th className="fw-semibold" width="40%">{t('general.title')}</th>
                  <th className="fw-semibold text-center">SCOPE</th>
                  <th className="fw-semibold text-center" width="10%">{t('general.evaluators')}</th>
                </tr>
              </thead>
              <tbody>
                {filterQuestions.map((question) => {
                  return <tr key={question.uuid}>
                    <td className="text-center">
                      {question.evaluators.length === 0 ? (
                        <span className="badge badge-square badge-danger" data-bs-toggle="tooltip" data-bs-placement="top" title={t('questions.no-posible')}></span>
                      ) : (
                        <input name="qs" value={question.uuid} onChange={() => handleOnChange(question)} className="form-check-input" type="checkbox" checked={selectedQuestions.find(q => q.uuid === question.uuid) !== undefined} />
                      )}
                    </td>
                    <td>{question.ref}</td>
                    <td>{question.title}</td>
                    <td className="text-center"><span className="badge badge-primary" data-bs-toggle="tooltip" data-bs-placement="top" title={question.scope.scope_name}>{question.scope.scope_ref}</span></td>
                    <td width="40%">
                      {usersIsLoaded && (
                        <Select options={selectOptions} isMulti onChange={(evaluators) => handleEvaluators(evaluators, question)}
                          defaultValue={getPosibleEvaluators(question.scope)}
                        />
                      )}
                    </td>
                  </tr>
                })}
              </tbody>
              {/* <tfoot>
                <tr>
                  <th colSpan="4">{filterQuestions.length}</th>
                </tr>
              </tfoot> */}
            </table>
          </div>
        )}
      </div>
    );
  }
}

export default SelectQuestions;
