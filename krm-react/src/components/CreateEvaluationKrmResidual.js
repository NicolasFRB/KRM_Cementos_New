import React from "react";
import { useState, useEffect } from "react";

import configService from "../services/config.js";

import SelectCompanies from "./SelectCompanies.js";
import SelectRisk from "./SelectRiskResidualKrm.js";
import EvaluationKrmInherentCreateSteps from "./EvaluationKrmInherentCreateSteps.js";

let $ = window.$;

function CreateEvaluationKrmInherent(props) {
  const [error, setError] = useState(null);

  const [riskCompaniesLoading, setRiskCompaniesLoading] = useState(false);
  const [selectedRisks, setSelectedRisks] = useState([]);
  const [selectedCompanies, setSelectedCompanies] = useState([]);
  const [riskCompanies, setRiskCompanies] = useState([]);
  const [companies, setCompanies] = useState([])

  const [riskCompaniesToEvaluate, setRiskCompaniesToEvaluate] = useState([]);

  const [formData, setFormData] = useState({ 'completed': false });

  const readFormData = () => {
    let newFormData = {};
    newFormData.ref = $('#e_ref').val();
    newFormData.date_begin = $('#e_date_begin').val();
    newFormData.date_intermediate = $('#e_date_intermediate').val();
    newFormData.date_end = $('#e_date_end').val();
    newFormData.description = $('#e_description').val();
    newFormData.completed = newFormData.ref !== '' && newFormData.date_begin !== '' && newFormData.date_intermediate !== '' && newFormData.date_end !== '';
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
          rs.risks.push(risk.pk);
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
      alert('Falta algún dato imprescindible en el formulario');
      return false;
    }
    if (selectedCompanies.length === 0) {
      alert('No se ha seleccionado ninguna empresa');
      return false;
    }
    if (riskCompaniesToEvaluate.length === 0) {
      alert('No se ha seleccionado ningún riesgo a evaluar');
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

  return (
    <div className="App">
      <div className="row">
        <div className="col-12">
          <h3 className="mb-6">Paso 2: Seleccione las compañías para evaluar</h3>
          {formData.completed === false && (
            <>
              <div className="alert alert-primary">Complete todos los datos obligatorios sobre la evaluación</div>
            </>
          )
          }
          <div className={(formData.completed ? '' : 'd-none')}>
            <SelectCompanies selectedCompanies={selectedCompanies} setSelectedCompanies={setSelectedCompanies} companies={companies} setCompanies={setCompanies} />
          </div>
          <div className="separator my-10"></div>
        </div>
        <div className="col-12">
          <h3 className="mb-5">Paso 3: Seleccione los Riesgos a evaluar</h3>
        </div>
        {selectedCompanies.length === 0 && (
          <>
            <div className="alert alert-primary">Seleccione al menos una compañía</div>
          </>
        )
        }
        <div className={"row " + (selectedCompanies.length ? '' : 'd-none')}>
          <div className="col col-12">
            <SelectRisk selectedRisks={selectedRisks} setSelectedRisks={setSelectedRisks} />
          </div>
        </div>
        <div className="separator my-10"></div>
        <div className="col-12" id="launch">
          <h3 className="mb-5">Paso 4: Resumen del lanzamiento</h3>
          {selectedRisks.length > 0 && (
            <>
              <div className="mt-5 mb-15">
                <p>
                  <button onClick={updateControls} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap" data-kt-indicator={riskCompaniesLoading ? 'on' : 'off'}>
                    <span className="indicator-label">Calcular los Tests de riesgo que se lanzarán</span>
                    <span className="indicator-progress">
                      Calculando...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                    </span>
                  </button>
                </p>
                <input type="hidden" name="risk_companies" value={JSON.stringify(riskCompaniesToEvaluate)} />
              </div>
              {!riskCompaniesLoading && (
                <div className="mt-5 mb-5">
                  {riskCompanies.map((company, index) => {
                    if (company.risks.length > 0) {
                      return <div key={index}>
                        <h4>Evaluación: {formData.ref} - {company.company.name}</h4>
                        <h5>Tests de Riesgo Inherente que se lanzarán</h5>
                        <table className="table table-striped customDatatable">
                          <thead>
                            <tr>
                              <th className="fw-semibold">&nbsp;</th>
                              <th className="fw-semibold">REF</th>
                              <th className="fw-semibold">NOMBRE</th>
                              <th className="fw-semibold">¿EVALUADO?</th>
                              <th className="fw-semibold">EVALUADOR ASIGNADO</th>
                            </tr>
                          </thead>
                          <tbody>
                            {company.risks.map((risk, index) => {
                              return <tr key={risk.pk}>
                                <td className="text-center">
                                  {(!risk.evaluated || risk.domain_risk_evaluator.length === 0) && (
                                    <span className="badge badge-square badge-danger" data-bs-toggle="tooltip" data-bs-placement="top" title="No es posible lanzar este test sin tener asignado previamente un experto para ese dominio de riesgo"></span>
                                  )}
                                  {risk.evaluated && risk.domain_risk_evaluator.length > 0 && (
                                    <input id={'ri' + risk.pk} onChange={() => selectRiskCompanyToEvaluate(risk.pk)} className="form-check-input" name="risks" type="checkbox" value={risk.pk} checked={risk.checked} />
                                  )}
                                </td>
                                <td><label htmlFor={'ri' + risk.pk}>{risk.risk_ref}</label></td>
                                <td><span className="fw-semibold ps-2 fs-6">{risk.name}</span></td>
                                <td className="text-center">
                                  {risk.evaluated && (
                                    <span className="badge badge-primary">Sí</span>
                                  )}
                                  {!risk.evaluated && (
                                    <span className="badge badge-danger">No</span>
                                  )}
                                </td>
                                <td>
                                  {risk.domain_risk_evaluator.map((evaluator, index) => {
                                    return (
                                      <>
                                        <div className="mb-1" key={index}>
                                          <span className="badge badge-primary" >{evaluator}</span>
                                        </div>
                                      </>
                                    )
                                  })}
                                  {risk.domain_risk_evaluator.length === 0 && (
                                    <>
                                      <span className="badge badge-danger">Sin asignar</span> <a rel="noreferrer" target="_blank" className="mb-3" href={`/${window.LANG}/companies/assign-evaluator/${risk.company_domain_risk_evaluator}/`}><span className="badge badge-primary">Asignar</span></a>
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
            <div className="alert alert-primary">Selecciona al menos un riesgo para poder lanzar la evaluación</div>
          )}
          {error && (
            <div className="alert alert-danger">{error}</div>
          )}
        </div>
        {riskCompaniesToEvaluate.length > 0 && (
          <div className="col-12">
            <button onClick={sendForm} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap" data-kt-indicator="off">
              <span className="indicator-label">Lanzar evaluaciones</span>
              <span className="indicator-progress">
                Lanzando...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
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
