import React from "react";
import { useEffect } from "react";
import ReactDOM from "react-dom";

function EvaluationCreateSteps(
  {
    selectedCompanies,
    formData,
    selectedDataRiskCompanies
  }
) {
  useEffect(() => {
  }, []);

  return (
    ReactDOM.createPortal(
      <div className="stepper-nav">
        <div className={"stepper-item " + (formData ? 'completed' : '')} data-kt-stepper-element="nav">
          <div className="stepper-wrapper">
            <div className="stepper-icon w-40px h-40px">
              <i className="stepper-check fas fa-check"></i>
              <span className="stepper-number">1</span>
            </div>
            <div className="stepper-label">
              <h3 className="stepper-title">Datos</h3>
            </div>
          </div>
          <div className="stepper-line h-40px"></div>
        </div>
        <div className={"stepper-item " + (selectedCompanies ? 'completed' : '')} data-kt-stepper-element="nav">
          <div className="stepper-wrapper">
            <div className="stepper-icon w-40px h-40px">
              <i className="stepper-check fas fa-check"></i>
              <span className="stepper-number">2</span>
            </div>
            <div className="stepper-label">
              <h3 className="stepper-title">Compañías</h3>
            </div>
          </div>
          <div className="stepper-line h-40px"></div>
        </div>
        <div className={"stepper-item " + (selectedDataRiskCompanies ? 'completed' : '')} data-kt-stepper-element="nav">
          <div className="stepper-wrapper">
            <div className="stepper-icon w-40px h-40px">
              <i className="stepper-check fas fa-check"></i>
              <span className="stepper-number">3</span>
            </div>
            <div className="stepper-label">
              <h3 className="stepper-title">Riesgos</h3>
            </div>
          </div>
          <div className="stepper-line h-40px"></div>
        </div>
        <div className="stepper-item pending" data-kt-stepper-element="nav">
          <div className="stepper-wrapper">
            <div className="stepper-icon w-40px h-40px">
              <i className="stepper-check fas fa-check"></i>
              <span className="stepper-number">5</span>
            </div>
            <div className="stepper-label">
              <h3 className="stepper-title">Lanzamiento</h3>
            </div>
          </div>
        </div>
      </div>
      ,
      document.getElementById("evaluationSteps")
    )
  );
}

export default EvaluationCreateSteps;
