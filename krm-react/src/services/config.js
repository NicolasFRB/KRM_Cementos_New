let base = "";
if (window.location.hostname.indexOf("localhost") > -1) {
  base = "http://localhost:8000";
} else if (window.location.hostname.indexOf("compliance.ofisat.net") > -1) {
  base = "https://compliance.ofisat.net";
} else if (window.location.hostname.indexOf("test.compliancetool.net") > -1) {
  base = "https://test.compliancetool.net";
} else {
  base = "https://gvi.compliancetool.net/";
}

const baseUrlApi = `${base}/api/`;

const user = window.$('#pk').data('pk');

const configService = {
  apiGetProcesses: `${baseUrlApi}process/`,
  apiGetRisks: `${baseUrlApi}risks/`,
  apiGetDomainRisks: `${baseUrlApi}domain-risks/`,
  apiGetControls: `${baseUrlApi}controls/`,
  apiGetCompanies: `${baseUrlApi}companies?user=${user}`,
  apiGetRiskCompany: `${baseUrlApi}riskscompany/`,
  apiGetRiskCompanyResidual: `${baseUrlApi}riskscompanyresidual/`,
  apiSendRiskTestInherent: `${baseUrlApi}risktestinherentexpert/`,
  apiSendRiskTestResidual: `${baseUrlApi}risktestresidualevaluator/`,
  apiSendRiskCompanyResidualAdmin: `${baseUrlApi}riskcompanyresidualadmin/`,
  apiGetControlCompany: `${baseUrlApi}controlscompany/`,
  apiGetQuestionnaires: `${baseUrlApi}questionnaires/`,
  apiGetQuestions: `${baseUrlApi}questions/`,
  apiGetUsers: `${baseUrlApi}users/`,
  apiSendQuestionTest: `${baseUrlApi}questiontest/`,

};

export default configService;
