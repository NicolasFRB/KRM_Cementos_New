import React from 'react';
import ReactDOM from 'react-dom/client';
import SelectControls from "./components/SelectControls";
import CreateEvaluationKrmInherent from './components/CreateEvaluationKrmInherent';


var krcEvaluationElement = document.getElementById("select-controls");
var krmEvaluationElement = document.getElementById("create-evaluation-krm-inherent");

if (krcEvaluationElement) {
  const KrcEvaluation = ReactDOM.createRoot(krcEvaluationElement);
  KrcEvaluation.render(
    <SelectControls />
  );
}

if (krmEvaluationElement) {
  const KrmEvaluation = ReactDOM.createRoot(krmEvaluationElement);
  KrmEvaluation.render(
    <CreateEvaluationKrmInherent />
  );
}


window.LANG = document.getElementsByTagName('html')[0].attributes[0].value;
