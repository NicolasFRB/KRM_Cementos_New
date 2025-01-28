let base = "http://localhost:8000";

// if (window.location.hostname.indexOf("krm-tool-uat") > -1) {
//   base = "https://krm-tool-uat.des-onprem1.eci.geci";
// } else if (window.location.hostname.indexOf("krm-tool-nft") > -1) {
//   base = "https://krm-tool-nft.pre-onprem1.eci.geci";
// } else if (window.location.hostname.indexOf("krm-tool.pro") > -1) {
//   base = "https://krm-tool.pro-onprem1.eci.geci";
// }

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
  apiGetControlPeriodicity: `${base}/es/api/controlperiodicity/`,
};

export default configService;
