import React from 'react';
import ReactDOM from 'react-dom/client';
import CreateEvaluationKrc from "./components/CreateEvaluationKrc";
import CreateEvaluationKrmInherent from './components/CreateEvaluationKrmInherent';
import RuRiskTestInherent from './components/krm_inherent/RuRiskTestInherent';
import CaRiskTestInherent from './components/krm_inherent/CaRiskTestInherent';


let krcEvaluationElement = document.getElementById("create-evaluation-krc");
let krmEvaluationElement = document.getElementById("create-evaluation-krm-inherent");
let risksTestInherent = document.getElementsByClassName("risk_test_inherent");
let adminRisksTestInherent = document.getElementsByClassName("admin_risk_test_inherent");


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

if (krmEvaluationElement) {
  const KrmEvaluation = ReactDOM.createRoot(krmEvaluationElement);
  KrmEvaluation.render(
    <CreateEvaluationKrmInherent />
  );
}


window.LANG = document.getElementsByTagName('html')[0].attributes[0].value;
