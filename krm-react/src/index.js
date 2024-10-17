import React from 'react';
import ReactDOM from 'react-dom/client';

import i18next from "i18next";
import { I18nextProvider } from "react-i18next";

import global_es from "./locales/es.json";
import global_en from "./locales/en.json";

import CreateEvaluationKrc from "./components/CreateEvaluationKrc";
import CreateEvaluationKrmInherent from './components/CreateEvaluationKrmInherent';
import CreateEvaluationKrmResidual from './components/CreateEvaluationKrmResidual';
import RuRiskTestInherent from './components/krm_inherent/RuRiskTestInherent';
import CaRiskTestInherent from './components/krm_inherent/CaRiskTestInherent';
import RuRiskTestResidual from './components/krm_inherent/RuRiskTestResidual';
import CaRiskTestResidual from './components/krm_inherent/CaRiskTestResidual';
import CreateEvaluationQuestionnaire from './components/CreateEvaluationQuestionnaire';
import RuQuestionTestComplete from './components/questionnaires/RuQuestionTest';


let lng = window.location.href.indexOf("/en/") > -1 ? 'en' : 'es';

i18next.init({
  interpolation: { escapeValue: false },  // React already does escaping
  lng: lng,                              // language to use
  resources: {
    es: {
      global: global_es
    },
    en: {
      global: global_en
    }
  }
})

let krcEvaluationElement = document.getElementById("create-evaluation-krc");
let krmEvaluationInherentElement = document.getElementById("create-evaluation-krm-inherent");
let krmEvaluationResiduallement = document.getElementById("create-evaluation-krm-residual");
let evaluationQuesqionnaireElement = document.getElementById("create-evaluation-questionnaire");
let risksTestInherent = document.getElementsByClassName("risk_test_inherent");
let adminRisksTestInherent = document.getElementsByClassName("admin_risk_test_inherent");
let risksTestResidual = document.getElementsByClassName("risk_test_residual");
let adminRisksTestResidual = document.getElementsByClassName("admin_risk_test_residual");
let ruQuestionTestComplete = document.getElementsByClassName("question_test");


for (let i = 0; i < risksTestInherent.length; i++) {
  let riskTestInherent = ReactDOM.createRoot(risksTestInherent.item(i));
  let pk = parseInt(risksTestInherent.item(i).getAttribute('data-risktestpk'));
  let impactContinuity = parseInt(risksTestInherent.item(i).getAttribute('data-impact-continuity'));
  let impactBranding = parseInt(risksTestInherent.item(i).getAttribute('data-impact-branding'));
  let impactEconomic = parseInt(risksTestInherent.item(i).getAttribute('data-impact-economic'));
  let probability = parseInt(risksTestInherent.item(i).getAttribute('data-probability'));
  let description = risksTestInherent.item(i).getAttribute('data-description');
  riskTestInherent.render(
    <I18nextProvider i18n={i18next}>
      <RuRiskTestInherent
        pk={pk}
        initialImpactBranding={impactBranding}
        initialImpactContinuity={impactContinuity}
        initialImpactEconomic={impactEconomic}
        initialProbability={probability}
        initialDescription={description}
      />
    </I18nextProvider>
  )
}

for (let i = 0; i < ruQuestionTestComplete.length; i++) {
  let ruQuestionTest = ReactDOM.createRoot(ruQuestionTestComplete.item(i));
  let pk = parseInt(ruQuestionTestComplete.item(i).getAttribute('data-questiontestpk'));
  let answer = parseInt(ruQuestionTestComplete.item(i).getAttribute('data-answer'));
  let description = ruQuestionTestComplete.item(i).getAttribute('data-description');
  ruQuestionTest.render(
    <I18nextProvider i18n={i18next}>
      <RuQuestionTestComplete pk={pk} initialAnswer={answer} initialDescription={description} />
    </I18nextProvider>
  )
}

for (let i = 0; i < adminRisksTestInherent.length; i++) {
  let riskTestInherent = ReactDOM.createRoot(adminRisksTestInherent.item(i));
  let pk = parseInt(adminRisksTestInherent.item(i).getAttribute('data-risktestpk'));
  let impact = parseInt(adminRisksTestInherent.item(i).getAttribute('data-impact'));
  let probability = parseInt(adminRisksTestInherent.item(i).getAttribute('data-probability'));
  let description = adminRisksTestInherent.item(i).getAttribute('data-description');
  riskTestInherent.render(
    <I18nextProvider i18n={i18next}>
      <CaRiskTestInherent pk={pk} initialImpact={impact} initialProbability={probability} initialDescriptionAdmin={description} />
    </I18nextProvider>
  )
}

if (krcEvaluationElement) {
  const KrcEvaluation = ReactDOM.createRoot(krcEvaluationElement);
  KrcEvaluation.render(
    <I18nextProvider i18n={i18next}>
      <CreateEvaluationKrc />
    </I18nextProvider>
  );
}

if (krmEvaluationInherentElement) {
  const krmEvaluationInherent = ReactDOM.createRoot(krmEvaluationInherentElement);
  krmEvaluationInherent.render(
    <I18nextProvider i18n={i18next}>
      <CreateEvaluationKrmInherent />
    </I18nextProvider>
  );
}

if (krmEvaluationResiduallement) {
  const KrmEvaluationResidual = ReactDOM.createRoot(krmEvaluationResiduallement);
  KrmEvaluationResidual.render(
    <I18nextProvider i18n={i18next}>
      <CreateEvaluationKrmResidual />
    </I18nextProvider>
  );
}

if (evaluationQuesqionnaireElement) {
  const EvaluationQuestionnaire = ReactDOM.createRoot(evaluationQuesqionnaireElement);
  EvaluationQuestionnaire.render(
    <I18nextProvider i18n={i18next}>
      <CreateEvaluationQuestionnaire />
    </I18nextProvider>
  );
}

for (let i = 0; i < risksTestResidual.length; i++) {
  let riskTestResidual = ReactDOM.createRoot(risksTestResidual.item(i));
  let pk = parseInt(risksTestResidual.item(i).getAttribute('data-risktestpk'));
  let probability = parseInt(risksTestResidual.item(i).getAttribute('data-probability'));
  let description = risksTestResidual.item(i).getAttribute('data-description');
  riskTestResidual.render(
    <I18nextProvider i18n={i18next}>
      <RuRiskTestResidual
        pk={pk}
        initialProbability={probability}
        initialDescription={description}
      />
    </I18nextProvider>
  )
}

for (let i = 0; i < adminRisksTestResidual.length; i++) {
  let riskTestResidual = ReactDOM.createRoot(adminRisksTestResidual.item(i));
  let pk = parseInt(adminRisksTestResidual.item(i).getAttribute('data-risktestpk'));
  let probability = parseInt(adminRisksTestResidual.item(i).getAttribute('data-probability'));
  let description = adminRisksTestResidual.item(i).getAttribute('data-description');
  riskTestResidual.render(
    <I18nextProvider i18n={i18next}>
      <CaRiskTestResidual pk={pk} initialProbability={probability} initialDescriptionAdmin={description} />
    </I18nextProvider>
  )

}

window.LANG = document.getElementsByTagName('html')[0].attributes[0].value;
