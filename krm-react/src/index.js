import React from 'react';
import ReactDOM from 'react-dom/client';
import CreateEvaluationKrc from "./components/CreateEvaluationKrc";
import CreateEvaluationKrmInherent from './components/CreateEvaluationKrmInherent';
import CreateEvaluationKrmResidual from './components/CreateEvaluationKrmResidual';
import RuRiskTestInherent from './components/krm_inherent/RuRiskTestInherent';
import CaRiskTestInherent from './components/krm_inherent/CaRiskTestInherent';
import RuRiskTestResidual from './components/krm_inherent/RuRiskTestResidual';
import CaRiskTestResidual from './components/krm_inherent/CaRiskTestResidual';


let krcEvaluationElement = document.getElementById("create-evaluation-krc");
let krmEvaluationInherentElement = document.getElementById("create-evaluation-krm-inherent");
let krmEvaluationResiduallement = document.getElementById("create-evaluation-krm-residual");
let risksTestInherent = document.getElementsByClassName("risk_test_inherent");
let adminRisksTestInherent = document.getElementsByClassName("admin_risk_test_inherent");
let risksTestResidual = document.getElementsByClassName("risk_test_residual");
let adminRisksTestResidual = document.getElementsByClassName("admin_risk_test_residual");


for (let i = 0; i < risksTestInherent.length; i++) {
  let riskTestInherent = ReactDOM.createRoot(risksTestInherent.item(i));
  let pk = parseInt(risksTestInherent.item(i).getAttribute('data-risktestpk'));
  let impactContinuity = parseInt(risksTestInherent.item(i).getAttribute('data-impact-continuity'));
  let impactBranding = parseInt(risksTestInherent.item(i).getAttribute('data-impact-branding'));
  let impactEconomic = parseInt(risksTestInherent.item(i).getAttribute('data-impact-economic'));
  let probability = parseInt(risksTestInherent.item(i).getAttribute('data-probability'));
  let description = risksTestInherent.item(i).getAttribute('data-description');
  riskTestInherent.render(
    <RuRiskTestInherent
      pk={pk}
      initialImpactBranding={impactBranding}
      initialImpactContinuity={impactContinuity}
      initialImpactEconomic={impactEconomic}
      initialProbability={probability}
      initialDescription={description}
    />
  )
}

for (let i = 0; i < adminRisksTestInherent.length; i++) {
  let riskTestInherent = ReactDOM.createRoot(adminRisksTestInherent.item(i));
  let pk = parseInt(adminRisksTestInherent.item(i).getAttribute('data-risktestpk'));
  let impact = parseInt(adminRisksTestInherent.item(i).getAttribute('data-impact'));
  let probability = parseInt(adminRisksTestInherent.item(i).getAttribute('data-probability'));
  let description = adminRisksTestInherent.item(i).getAttribute('data-description');
  riskTestInherent.render(
    <CaRiskTestInherent pk={pk} initialImpact={impact} initialProbability={probability} initialDescriptionAdmin={description} />
  )
}

if (krcEvaluationElement) {
  const KrcEvaluation = ReactDOM.createRoot(krcEvaluationElement);
  KrcEvaluation.render(
    <CreateEvaluationKrc />
  );
}

if (krmEvaluationInherentElement) {
  const krmEvaluationInherent = ReactDOM.createRoot(krmEvaluationInherentElement);
  krmEvaluationInherent.render(
    <CreateEvaluationKrmInherent />
  );
}

if (krmEvaluationResiduallement) {
  const KrmEvaluationResidual = ReactDOM.createRoot(krmEvaluationResiduallement);
  KrmEvaluationResidual.render(
    <CreateEvaluationKrmResidual />
  );
}

for (let i = 0; i < risksTestResidual.length; i++) {
  let riskTestResidual = ReactDOM.createRoot(risksTestResidual.item(i));
  let pk = parseInt(risksTestResidual.item(i).getAttribute('data-risktestpk'));
  let probability = parseInt(risksTestResidual.item(i).getAttribute('data-probability'));
  let description = risksTestResidual.item(i).getAttribute('data-description');
  riskTestResidual.render(
    <RuRiskTestResidual
      pk={pk}
      initialProbability={probability}
      initialDescription={description}
    />
  )
}

for (let i = 0; i < adminRisksTestResidual.length; i++) {
  let riskTestResidual = ReactDOM.createRoot(adminRisksTestResidual.item(i));
  let pk = parseInt(adminRisksTestResidual.item(i).getAttribute('data-risktestpk'));
  let probability = parseInt(adminRisksTestResidual.item(i).getAttribute('data-probability'));
  let description = adminRisksTestResidual.item(i).getAttribute('data-description');
  riskTestResidual.render(
    <CaRiskTestResidual pk={pk} initialProbability={probability} initialDescriptionAdmin={description} />
  )
}

window.LANG = document.getElementsByTagName('html')[0].attributes[0].value;
