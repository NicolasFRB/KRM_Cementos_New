import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import Select from 'react-select'

function SelectControlsCompanyKrc(
  {
    selectedDomainRisks,
    selectedProcesses,
    selectedScopes,
    selectedCompanies,
    selectedPeriodicity,
    // selectedRisks,
    keyControl,
    elc,
    controlsToEvaluate,
    setControlsToEvaluate,
  }) {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [controlsCompany, setControlsCompany] = useState([]);

  const [t] = useTranslation("global");

  const isSelectedControl = (companyPk, controlPk) => {
    for (let i = 0; i < controlsToEvaluate.length; i++) {
      if (controlsToEvaluate[i].cs.includes(controlPk)) {
        return true;
      }
    }
    return false;
  }

  const selectControlCompanyToEvaluate = (companyPk, controlPk) => {
    let newControlsCompanyToEvaluate = controlsToEvaluate;

    newControlsCompanyToEvaluate = newControlsCompanyToEvaluate.map((controlCompany) => {
      if (controlCompany.c === companyPk) {
        if (controlCompany.cs.includes(controlPk)) {
          controlCompany.cs = controlCompany.cs.filter(function (value, index, arr) {
            return value !== controlPk;
          });
          controlCompany.csData = controlCompany.csData.filter(function (value, index, arr) {
            return value.pk !== controlPk;
          });
        } else {
          controlCompany.cs.push(controlPk);
          controlCompany.csData.push({
            pk: controlPk,
            owners: getPosibleOwners(companyPk, controlPk),
            supervisors: getPosibleSupervisors(companyPk, controlPk),
            ownersSelected: getPosibleOwners(companyPk, controlPk),
            supervisorsSelected: getPosibleSupervisors(companyPk, controlPk)
          })
        }
      }
      return controlCompany;
    });

    setControlsToEvaluate(newControlsCompanyToEvaluate);
  };

  const getPosibleOwners = (companyPk, controlPk) => {
    let controlToEvaluate = controlsCompany.filter(controlCompany => controlCompany.c.pk === companyPk);
    let control = controlToEvaluate[0].cs.filter(control => control.control.pk === controlPk);
    return control[0].control_test_owners;
  }

  const getPosibleSupervisors = (companyPk, controlPk) => {
    let controlToEvaluate = controlsCompany.filter(controlCompany => controlCompany.c.pk === companyPk);
    let control = controlToEvaluate[0].cs.filter(control => control.control.pk === controlPk);
    return control[0].control_test_supervisors;
  }


  const truncate = function (str) {
    return str.length > 100 ? str.substring(0, 100) + "..." : str;
  }


  const updateControls = (e) => {
    if (e) {
      e.preventDefault();
    }
    setIsLoading(true);
    if (selectedCompanies.length > 0) {
      const params = {
        company_pks: selectedCompanies,
        risk_pks: [],
        elc: elc,
        key_control: keyControl,
        process_pks: selectedProcesses,
        scopes: selectedScopes,
        domain_risk_pks: selectedDomainRisks,
        control_frequency: selectedPeriodicity,
      };

      var url = new URL(configService.apiGetControlCompany);
      for (let k in params) {
        url.searchParams.append(k, params[k]);
      }

      fetch(url)
        .then((res) => res.json())
        .then(
          (res) => {
            let newControlsCompanyToEvaluate = res.map((item) => {
              return (
                {
                  c: item.c.pk,
                  cs: [],
                  csData: []
                }
              )
            });
            setControlsToEvaluate(newControlsCompanyToEvaluate);
            setControlsCompany(res);
            setIsLoading(false);
          },
          (error) => {
            setIsLoading(false);
            setError(error);
          }
        );
    } else {
      setIsLoading(false);
    }
  }

  const setOwners = (owners, company_pk, control_pk) => {
    let newControlsToEvaluate = controlsToEvaluate;

    newControlsToEvaluate = newControlsToEvaluate.map((controlCompany) => {
      if (controlCompany.c === company_pk) {
        controlCompany.csData.forEach((controlData) => {
          if (controlData.pk === control_pk) {
            controlData.ownersSelected = owners;
          }
        });
      }
      return controlCompany;
    });
    setControlsToEvaluate(newControlsToEvaluate);
  }

  const setSupervisors = (supervisors, company_pk, control_pk) => {
    let newControlsToEvaluate = controlsToEvaluate;

    newControlsToEvaluate = newControlsToEvaluate.map((controlCompany) => {
      if (controlCompany.c === company_pk) {
        controlCompany.csData.forEach((controlData) => {
          if (controlData.pk === control_pk) {
            controlData.supervisorsSelected = supervisors;
          }
        });
      }
      return controlCompany;
    });

    setControlsToEvaluate(newControlsToEvaluate);
  }

  const selectAll = (companyPk) => {
    let newControlsToEvaluate = controlsToEvaluate.map((controlToEvaluate) => {
      if (controlToEvaluate.c === companyPk) {
        for (let i = 0; i < controlsCompany.length; i++) {
          if (controlsCompany[i].c.pk === companyPk) {

            for (let j = 0; j < controlsCompany[i].cs.length; j++) {
              selectControlCompanyToEvaluate(companyPk, controlsCompany[i].cs[j].control.pk)
            }

            // controlToEvaluate.cs = controlsCompany[i].cs.map((cc) => {
            //   selectControlCompanyToEvaluate(companyPk, cc.pk)

            //   // return cc.pk;
            // })
          }
        }
        // controlToEvaluate.cs = controlsCompany.filter(controlCompany => controlCompany.c.pk === companyPk)[0].cs.map((cc) => {
        //   return cc.control.pk;
        // });

        // selectControlCompanyToEvaluate(companyPk company_control.control.pk)
        return controlToEvaluate;
      } else {
        return controlToEvaluate
      }
    })
    setControlsToEvaluate(newControlsToEvaluate);
  };

  const unSelectAll = (companyPk) => {
    let newControlsToEvaluate = controlsToEvaluate.map((controlToEvaluate) => {
      if (controlToEvaluate.c === companyPk) {
        controlToEvaluate.cs = [];
        controlToEvaluate.csData = [];
        return controlToEvaluate;
      } else {
        return controlToEvaluate
      }
    })
    setControlsToEvaluate(newControlsToEvaluate);
  };

  const checkControlInCompanyControlToEvaluate = (companyPk, controlPk) => {
    for (let i = 0; i < controlsToEvaluate.length; i++) {
      if (controlsToEvaluate[i].c === companyPk) {
        if (controlsToEvaluate[i].cs.includes(controlPk)) {
          return true;
        }
      }
    }
    return false;
  };

  useEffect(() => {
    window.CustomDatatables.destroy();
    // window.CustomDatatables.init();
    window.CustomDatatables.initEvalKrc();
  }, [controlsCompany]);

  if (error) {
    return <div>Error: {error.message}</div>;
  } else {
    return (
      <div>
        {selectedCompanies.length > 0 && (
          <div className="mt-5 mb-5">
            <button onClick={updateControls} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap mb-7" data-kt-indicator={isLoading ? 'on' : 'off'}>
              <span className="indicator-label">{t('selectcontrol.calc-controls')}</span>
              <span className="indicator-progress">
                {t('selectcontrol.loading')}...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
              </span>
            </button>
            {!isLoading && controlsCompany.map((company, index) => {
              return <div key={index} className="mt-5 mb-5">
                <h4>{t('selectcontrols.evaluations-for')} {company.c.name}</h4>
                <h5>{t('selectcontrols.control-to-launch')}</h5>
                {company.cs.length > 0 && (
                  <table className="table table-striped" id="riskkrc">
                    <thead>
                      <tr>
                        <th className="text-center">
                          <span onClick={() => selectAll(company.c.pk)} className=""><i className="bi bi-clipboard-check"></i></span>
                        </th>
                        <th className="fw-semibold">{t('general.ref')}</th>
                        <th className="fw-semibold" width="30%">{t('general.description')}</th>
                        <th className="fw-semibold text-center">{t('general.key')}</th>
                        <th className="fw-semibold text-center">{t('general.elc')}</th>
                        <th className="fw-semibold text-center" width="20%">{t('general.owner')}</th>
                        <th className="fw-semibold text-center" width="20%">{t('general.supervisor')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {company.cs.map((company_control, index) => {
                        return <tr key={company_control.control.pk}>
                          <td className="text-center">
                            <input id={'com' + company.c.pk + 'co' + company_control.control.pk} onChange={() => selectControlCompanyToEvaluate(company.c.pk, company_control.control.pk)} className="form-check-input" name="controls" type="checkbox" value={company_control.control.pk} checked={checkControlInCompanyControlToEvaluate(company.c.pk, company_control.control.pk)} />
                          </td>
                          <td><label htmlFor={'com' + company.c.pk + 'co' + company_control.control.pk}>{company_control.control.ref}</label></td>
                          <td><span dangerouslySetInnerHTML={{ __html: truncate(company_control.control.description) }}></span></td>
                          <td className="text-center">
                            {company_control.control.key_control && (
                              <span className="badge badge-primary">{t('general.yes')}</span>
                            )}
                            {!company_control.control.key_control && (
                              <span className="badge badge-danger">{t('general.no')}</span>
                            )}
                          </td>
                          <td className="text-center">
                            {company_control.control.is_elc && (
                              <span className="badge badge-primary">{t('general.yes')}</span>
                            )}
                            {!company_control.control.is_elc && (
                              <span className="badge badge-danger">{t('general.no')}</span>
                            )}
                          </td>
                          <td>
                            {isSelectedControl(company.c.pk, company_control.control.pk) && (
                              <Select
                                onChange={(owners) => setOwners(owners, company.c.pk, company_control.control.pk)}
                                getOptionValue={(option) => `${option['pk']}`}
                                options={company.c.employees.map((employee) => {
                                  return { pk: employee.pk, label: employee.email }
                                })}
                                isMulti
                                defaultValue={company_control.control_test_owners.map((owner) => {
                                  return { pk: owner.pk, label: owner.email }
                                })} />
                            )}
                          </td>
                          <td>
                            {isSelectedControl(company.c.pk, company_control.control.pk) && (
                              <Select
                                onChange={(supervisors) => setSupervisors(supervisors, company.c.pk, company_control.control.pk)}
                                getOptionValue={(option) => `${option['pk']}`}
                                options={company.c.employees.map((employee) => {
                                  return { pk: employee.pk, label: employee.email }
                                })}
                                isMulti
                                defaultValue={company_control.control_test_supervisors.map((owner) => {
                                  return { pk: owner.pk, label: owner.email }
                                })} />
                            )}
                          </td>
                        </tr>
                      })}
                    </tbody>
                  </table>
                )}

                {company.cs.length === 0 && (
                  <div key={index} className="alert alert-primary mt-5">{t('selectcontrol.nothing-to-evaluate')} {company.c.name}</div>
                )}
                {index < controlsCompany.length - 1 && (
                  <div className="separator my-10"></div>
                )}
              </div>
            })}
          </div>
        )}
        {selectedCompanies.length === 0 && (
          <div className="alert alert-primary">{t('selectcontrol.select-company')}</div>
        )}
      </div>
    );
  }
}

export default SelectControlsCompanyKrc;
