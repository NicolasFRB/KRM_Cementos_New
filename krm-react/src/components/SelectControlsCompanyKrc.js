import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectControlsCompanyKrc(
  {
    selectedDomainRisks,
    selectedProcesses,
    selectedCompanies,
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

  const selectControlCompanyToEvaluate = (companyPk, controlPk) => {
    let newControlsCompanyToEvaluate = controlsToEvaluate;

    newControlsCompanyToEvaluate = newControlsCompanyToEvaluate.map((controlCompany) => {
      if (controlCompany.c === companyPk) {
        if (controlCompany.cs.includes(controlPk)) {
          controlCompany.cs = controlCompany.cs.filter(function (value, index, arr) {
            return value !== controlPk;
          });
        } else {
          controlCompany.cs.push(controlPk);
        }
      }
      return controlCompany;
    });

    setControlsToEvaluate(newControlsCompanyToEvaluate);
  };

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
        domain_risk_pks: selectedDomainRisks
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
                  cs: []
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

  const selectAll = (companyPk) => {
    let newControlsToEvaluate = controlsToEvaluate.map((controlToEvaluate) => {
      if (controlToEvaluate.c === companyPk) {
        for (let i = 0; i < controlsCompany.length; i++) {
          if (controlsCompany[i].c.pk === companyPk) {
            controlToEvaluate.cs = controlsCompany[i].cs.map((cc) => {
              return cc.pk;
            })
          }
        }
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
        return controlToEvaluate;
      } else {
        return controlToEvaluate
      }
    })
    setControlsToEvaluate(newControlsToEvaluate);
  };

  const checkControlInCompanyControlToEvaluate = (companyPk, controlPk) => {
    console.log(companyPk);
    console.log(controlPk);
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
    window.CustomDatatables.init();
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
                  <table className="table table-striped customDatatable">
                    <thead>
                      <tr>
                        <th className="text-center">
                          <span onClick={() => selectAll(company.c.pk)} className="me-5"><i className="bi bi-clipboard-check"></i></span>
                          <span onClick={() => unSelectAll(company.c.pk)}><i className="bi bi-clipboard"></i></span>
                        </th>
                        <th className="fw-semibold">REF</th>
                        <th className="fw-semibold">{t('general.description')}</th>
                        <th className="fw-semibold text-center">KEY CONTROL</th>
                        <th className="fw-semibold text-center">ELC</th>
                      </tr>
                    </thead>
                    <tbody>
                      {company.cs.map((control, index) => {
                        return <tr key={control.pk}>
                          <td className="text-center">
                            <input id={'com' + company.c.pk + 'co' + control.pk} onChange={() => selectControlCompanyToEvaluate(company.c.pk, control.pk)} className="form-check-input" name="controls" type="checkbox" value={control.pk} checked={checkControlInCompanyControlToEvaluate(company.c.pk, control.pk)} />
                          </td>
                          <td><label htmlFor={'com' + company.c.pk + 'co' + control.pk}>{control.ref}</label></td>
                          <td><span dangerouslySetInnerHTML={{ __html: control.name }}></span></td>
                          <td className="text-center">
                            {control.key_control && (
                              <span className="badge badge-primary">{t('general.yes')}</span>
                            )}
                            {!control.key_control && (
                              <span className="badge badge-danger">{t('general.no')}</span>
                            )}
                          </td>
                          <td className="text-center">
                            {control.is_elc && (
                              <span className="badge badge-primary">{t('general.yes')}</span>
                            )}
                            {!control.is_elc && (
                              <span className="badge badge-danger">{t('general.no')}</span>
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
