import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

import configService from "../services/config.js";

import SelectCompanies from "./SelectCompanies.js";
// import SelectRisk from "./SelectRiskResidualKrm.js";
import SelectRisk from "./SelectRiskInherentKrm.js";
import EvaluationKrmInherentCreateSteps from "./EvaluationKrmInherentCreateSteps.js";
import SelectDomainRiskKrmInherent from "./SelectDomainRiskKrmInherent.js";

import Select from 'react-select'

let $ = window.$;

function CreateEvaluationKrmInherent(props) {
  const [error, setError] = useState(null);

  const [riskCompaniesLoading, setRiskCompaniesLoading] = useState(false);
  const [selectedRisks, setSelectedRisks] = useState([]);
  const [selectedDomainRisks, setSelectedDomainRisks] = useState([]);
  const [selectedCompanies, setSelectedCompanies] = useState([]);
  const [riskCompanies, setRiskCompanies] = useState([]);
  const [companies, setCompanies] = useState([])

  const [riskCompaniesToEvaluate, setRiskCompaniesToEvaluate] = useState([]);

  const [formData, setFormData] = useState({ 'completed': false });

  const [t] = useTranslation("global");

  const readFormData = () => {
    let newFormData = {};
    newFormData.ref = $('#e_ref').val();
    newFormData.date_begin = $('#e_date_begin').val();
    newFormData.date_end = $('#e_date_end').val();
    newFormData.description = $('#e_description').val();
    $('#error-e-date-begin, #error-e-date-end').addClass('d-none');
    const beginDate = new Date(newFormData.date_begin);
    const endDate = new Date(newFormData.date_end);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const datesOk = !isNaN(beginDate) && !isNaN(endDate) && beginDate <= endDate && beginDate >= today;

    if (beginDate> endDate) {
      $('#error-e-date-end').text(t("krmResidual.error-end-date")).removeClass('d-none');
      $('html, body').animate({
        scrollTop: $('#e_date_end').offset().top - 100
      }, 1000);
    } else if (beginDate< today) {
      $('#error-e-date-begin').text(t("krmResidual.error-start-date")).removeClass('d-none');
      $('html, body').animate({
        scrollTop: $('#e_date_begin').offset().top - 100
      }, 1000);
    } else {
      $('#error-e-date-begin, #error-e-date-end').text('').addClass('d-none');
    }
    newFormData.completed = newFormData.ref !== '' &&
                            newFormData.date_begin !== '' &&
                            newFormData.date_end !== '' &&
                            datesOk;
    setFormData(newFormData);
  }

  useEffect(() => {
    $('#e_ref, #e_date_begin, #e_date_intermediate, #e_date_end, #e_description').on('change', readFormData);
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    window.CustomDatatables.destroy();
    window.CustomDatatables.init();
  }, [riskCompaniesLoading]);

  const selectAll = (companyPk) => {
    let newRiskCompaniesToEvaluate = [];
    const newRiskCompanies = riskCompanies.map(rc => {
      if (rc.company.pk === companyPk) {
        rc.risks = rc.risks.map((risk) => {
          risk.checked = true;
          return risk;
        })
      }
      return rc;
    });
    setRiskCompanies(newRiskCompanies);

    // Quitamos esa compañía de los evaluados y luego la metemos con todo
    newRiskCompaniesToEvaluate = riskCompaniesToEvaluate.filter((rcte) => rcte.company_pk !== companyPk);

    newRiskCompanies.forEach(function (rc, i) {
      if (rc.company.pk === companyPk) {
        let risksChecked = rc.risks.filter((risk) => risk.domain_risk_evaluator.length > 0 && risk.evaluated);
        if (risksChecked.length > 0) {
          newRiskCompaniesToEvaluate.push(
            {
              company_pk: companyPk,
              risks: risksChecked.map((risk) => risk.pk)
            }
          )
        }
      }
    });

    setRiskCompaniesToEvaluate(newRiskCompaniesToEvaluate);
  };

  const unSelectAll = (companyPk) => {

    const newRiskCompanies = riskCompanies.map(rc => {
      if (rc.company.pk === companyPk) {
        rc.risks = rc.risks.map((risk) => {
          risk.checked = false;
          return risk;
        })
      }
      return rc;
    });
    setRiskCompanies(newRiskCompanies);
    setRiskCompaniesToEvaluate(riskCompaniesToEvaluate.filter((rcte) => rcte.company_pk !== companyPk));
  };

  const selectRiskCompanyToEvaluate = (pk) => {
    const newRiskCompanies = riskCompanies.map(c => {
      const newRiskCompany = c.risks.map(r => {
        if (r.pk === pk) {
          return { ...r, checked: !r.checked };
        }
        return r;
      });
      return { ...c, risks: newRiskCompany };
    });
    setRiskCompanies(newRiskCompanies);

    let riskSelect = [];
    // este array dispondrá de una lista de objetos donde venga la clave primaria de la compañía y el array de riesgos a lanzar
    newRiskCompanies.forEach(c => {
      let rs = {
        'company_pk': c.company.pk,
        'risks': []
      }
      c.risks.forEach(risk => {
        if (risk.checked) {
          rs.risks.push([risk.pk, risk.evaluator]);
        }
      });
      if (rs.risks.length > 0) {
        riskSelect.push(rs);
      }
    });
    setRiskCompaniesToEvaluate(riskSelect)
  }

  const sendForm = (e) => {
    e.preventDefault();
    if (formData.completed === false) {
      alert(t('krmResidual.form-incomplete'));
      return false;
    }
    if (selectedCompanies.length === 0) {
      alert(t('krmResidual.no-company-selected'));
      return false;
    }
    if (riskCompaniesToEvaluate.length === 0) {
      alert(t('krmResidual.no-risks-to-evaluate'));
      return false;
    }

    $(e.currentTarget).attr('data-kt-indicator', 'on');
    document.getElementById("evaluation_krm_create").submit();
  }

  const updateControls = (e) => {
    e.preventDefault();
    setRiskCompaniesLoading(true);
    setRiskCompaniesToEvaluate([]);

    const params = {
      company_pks: selectedCompanies,
      risk_pks: selectedRisks
    };


    var url = new URL(configService.apiGetRiskCompanyResidual);
    for (let k in params) {
      url.searchParams.append(k, params[k]);
    }

    fetch(url)
      .then((res) => res.json())
      .then(
        (res) => {
          let dataWithChecked = res.map(company => {
            let risksWithChecked = company.risks.map(risk => {
              return { ...risk, checked: false };
            });
            return {
              company: company.company,
              risks: risksWithChecked
            };
          })
          setRiskCompanies(dataWithChecked);
          setRiskCompaniesLoading(false);
          $('html, body').animate({
            scrollTop: $('#launch').offset().top - 100
          }, 1000);
        },
        (error) => {
          setError(error);
          setRiskCompaniesLoading(false);
        }
      );
  }

  const selectEvaluator = (selected_riskCompany, selected_risk, selected_evaluator_data) => {
    const newRiskCompanies = riskCompanies.map(c => {
      if (c.company.pk === selected_riskCompany.company.pk) {
        const updatedRisks = c.risks.map(risk => {
          if (risk.pk === selected_risk.pk) {
            return {
              ...risk,
              original_evaluator: risk.hasOwnProperty("original_evaluator") ? risk.original_evaluator : risk.evaluator,
              evaluator: selected_evaluator_data.pk,
              evaluator_data: {
                pk: selected_evaluator_data.pk,
                email: selected_evaluator_data.label,
              },
              save_evaluator: selected_evaluator_data.pk !== risk.evaluator
            };
          }
          return risk;
        });

        return { ...c, risks: updatedRisks };
      }
      return c;
    });

    setRiskCompanies(newRiskCompanies);

    let riskSelect = [];

    newRiskCompanies.forEach(c => {
      let rs = {
        company_pk: c.company.pk,
        risks: []
      };

      c.risks.forEach(risk => {
        if (risk.checked) {
          rs.risks.push([risk.pk, risk.evaluator]);
        }
      });

      if (rs.risks.length > 0) {
        riskSelect.push(rs);
      }
    });

    setRiskCompaniesToEvaluate(riskSelect);
  };

  // const selectEvaluator = (selected_riskCompany, selected_risk, selected_evaluator_data) => {

  //   setRiskCompanies((riskCompanies) =>
  //     riskCompanies.map((riskCompany) => {
  //       console.log(riskCompany);
  //       if(riskCompany.company.pk === selected_riskCompany.company.pk)
  //         return { ...riskCompany,
  //           risks: riskCompany.risks.map( (risk) => {
  //               if (risk.pk === selected_risk.pk) {
  //                 console.log(risk);
  //                 console.log({
  //                   ...risk,
  //                   original_evaluator: risk.hasOwnProperty("original_evaluator")? risk.original_evaluator: risk.evaluator,
  //                   evaluator: selected_evaluator_data.pk,
  //                   evaluator_data: {
  //                     pk:selected_evaluator_data.pk,
  //                     email:selected_evaluator_data.label,
  //                   },
  //                   save_evaluator: selected_evaluator_data.pk != risk.evaluator
  //                 });
  //                 return {
  //                   ...risk,
  //                   original_evaluator: risk.hasOwnProperty("original_evaluator")? risk.original_evaluator: risk.evaluator,
  //                   evaluator: selected_evaluator_data.pk,
  //                   evaluator_data: {
  //                     pk:selected_evaluator_data.pk,
  //                     email:selected_evaluator_data.label,
  //                   },
  //                   save_evaluator: selected_evaluator_data.pk != risk.evaluator
  //                 };

  //               }
  //               else return risk;
  //             })
  //         }
  //       else return riskCompany;
  //     })
  //   )
  // }

  return (
    <div className="App">
      <div className="row">
        <div className="col-12">
          <h3 className="mb-6">{t('krmResidual.step-2')}</h3>
          {formData.completed === false && (
            <>
              <div className="alert alert-primary">{t('krmResidual.evaluation-data-incomplete')}</div>
            </>
          )}
          <div className={(formData.completed ? '' : 'd-none')}>
            <SelectCompanies selectedCompanies={selectedCompanies} setSelectedCompanies={setSelectedCompanies} companies={companies} setCompanies={setCompanies} />
          </div>
        </div>
        <div className="separator my-10"></div>

        <div className="col-12">
          <h3 className="mb-6">{t('krmResidual.step-3')}</h3>
          {selectedCompanies.length === 0 && (
            <>
              <div className="alert alert-primary">{t('krmInherent.select-company')}</div>
            </>
          )
          }
          <div className={"row " + (selectedCompanies.length ? '' : 'd-none')}>
            <div className="col col-12 col-md-3">
              <SelectDomainRiskKrmInherent selectedCompanies={selectedCompanies} selectedDomainRisks={selectedDomainRisks} setSelectedDomainRisks={setSelectedDomainRisks} />
            </div>
          </div>
        </div>

        <div className="separator my-10"></div>
        <div className="col-12">
          <h3 className="mb-6">{t('krmResidual.step-4')}</h3>
          {selectedCompanies.length === 0 && (
            <>
              <div className="alert alert-primary">{t('krmResidual.select-company')}</div>
            </>
          )
          }
          <div className={"row " + (selectedCompanies.length ? '' : 'd-none')}>
            <div className="col col-12">
              <SelectRisk selectedRisks={selectedRisks} setSelectedRisks={setSelectedRisks} selectedDomainRisks={selectedDomainRisks} selectedCompanies={selectedCompanies}  />
            </div>
          </div>
        </div>

        <div className="separator my-10"></div>
        <div className="col-12" id="launch">
          <h3 className="mb-6">{t('krmResidual.step-5')}</h3>
          {selectedRisks.length > 0 && (
            <>
              <div className="mt-5 mb-15">
                <p>
                  <button onClick={updateControls} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap" data-kt-indicator={riskCompaniesLoading ? 'on' : 'off'}>
                    <span className="indicator-label">{t('krmResidual.calc-tests')}</span>
                    <span className="indicator-progress">
                      {t('krmResidual.loading')}...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                    </span>
                  </button>
                </p>
                <input type="hidden" name="risk_companies" value={JSON.stringify(riskCompaniesToEvaluate)} />
              </div>
              {!riskCompaniesLoading && (
                <div className="mt-5 mb-5">
                  {riskCompanies.map((company, index) => {
                    if (company.risks.length > 0) {
                      return <div key={company.company.pk}>
                        <h4>{t('krmResidual.evaluation')}: {formData.ref} - {company.company.name}</h4>
                        <h5>{t('krmResidual.tests-inherent-to-launch')}</h5>
                        <table className="table table-striped customDatatable">
                          <thead>
                            <tr>
                              <th className="text-center">
                                <span onClick={() => selectAll(company.company.pk)} className="me-5"><i className="bi bi-clipboard-check"></i></span>
                                <span onClick={() => unSelectAll(company.company.pk)}><i className="bi bi-clipboard"></i></span>
                              </th>
                              <th className="fw-semibold">{t('krmResidual.ref')}</th>
                              <th className="fw-semibold">{t('krmResidual.name')}</th>
                              <th className="fw-semibold text-center">{t('krmResidual.evaluate')}</th>
                              <th className="fw-semibold text-center">{t('krmResidual.expert-severity')}</th>
                              <th className="fw-semibold text-center">{t('krmResidual.severity-admin')}</th>
                              <th className="fw-semibold">{t('krmResidual.evaluator-assign')}</th>
                            </tr>
                          </thead>
                          <tbody>
                            {company.risks.map((risk, index) => {
                              return <tr key={risk.pk}>
                                <td className="text-center">
                                  {(!risk.evaluator) && (
                                    <span className="badge badge-square badge-danger" data-bs-toggle="tooltip" data-bs-placement="top" title="No es posible lanzar este test sin tener asignado previamente un evaluador"></span>
                                  )}
                                  {risk.evaluator && (
                                    <input id={'ri' + risk.pk} onChange={() => selectRiskCompanyToEvaluate(risk.pk)} className="form-check-input" name="risks" type="checkbox" value={risk.pk} checked={risk.checked} />
                                  )}
                                </td>
                                <td><label htmlFor={'ri' + risk.pk}>{risk.risk_ref}</label></td>
                                <td><span className="fw-semibold ps-2 fs-6">{risk.risk_name}</span></td>
                                <td className="text-center">
                                  {risk.evaluated && (
                                    <span className="badge badge-primary">Sí</span>
                                  )}
                                  {!risk.evaluated && (
                                    <span className="badge badge-danger">No</span>
                                  )}
                                </td>
                                <td className="text-center">
                                  <span className="badge badge-secondary">{risk.severity_evaluator_qualitative}</span>
                                </td>
                                <td className="text-center">
                                  <span className="badge badge-secondary">{risk.severity_administrator_qualitative}</span>
                                </td>
                                <td>
                                  { risk.evaluator && (
                                    <>
                                      <Select
                                        onChange={(evaluator) => selectEvaluator(company, risk, evaluator)}
                                        getOptionValue={(option) => `${option['pk']}`}
                                        options={company.company.employees.map((employee) => {
                                          // console.log(employee)
                                          return { pk: employee.pk, label: employee.email }
                                        })}
                                        // isMulti
                                        defaultValue={ risk?.evaluator_data ? {pk: risk.evaluator_data.pk, label: risk.evaluator_data.email}: null }

                                      />
                                    </>
                                  )}
                                  {!risk.evaluator && (
                                    // <>
                                    //   <span className="badge badge-danger">{t('krmResidual.without-assign')}</span> <a rel="noreferrer" target="_blank" className="mb-3" href={`/${window.LANG}/companies/assign-evaluator/${risk.company_domain_risk_evaluator}/`}><span className="badge badge-primary">{t('krmResidual.assign')}</span></a>
                                    // </>
                                    <>
                                      <Select
                                        onChange={(evaluator) => selectEvaluator(company, risk, evaluator)}
                                        getOptionValue={(option) => `${option['pk']}`}
                                        options={company.company.employees.map((employee) => {
                                          // console.log(employee)
                                          return { pk: employee.pk, label: employee.email }
                                        })}
                                        // isMulti
                                        defaultValue={ risk?.evaluator_data ? {pk: risk.evaluator_data.pk, label: risk.evaluator_data.email}: null }

                                      />
                                    </>
                                  )}
                                </td>
                              </tr>
                            })}
                          </tbody>
                        </table>
                        <div className="separator my-10"></div>
                      </div>
                    } else {
                      return false;
                    }
                  })}
                </div>
              )}
            </>
          )}
          {selectedRisks.length === 0 && (
            <div className="alert alert-primary">{t('krmResidual.select-risk')}</div>
          )}
          {error && (
            <div className="alert alert-danger">{error}</div>
          )}
        </div>
        {riskCompaniesToEvaluate.length > 0 && (
          <div className="col-12">
            <button onClick={sendForm} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap" data-kt-indicator="off">
              <span className="indicator-label">{t('krmResidual.launch-evaluation')}</span>
              <span className="indicator-progress">
                {t('krmResidual.launching')}...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
              </span>
            </button>
          </div>
        )}
      </div>
      <EvaluationKrmInherentCreateSteps
        selectedCompanies={selectedCompanies.length > 0}
        formData={formData.completed}
        selectedDataRiskCompanies={selectedRisks.length > 0} />
    </div>
  );
}

export default CreateEvaluationKrmInherent;
