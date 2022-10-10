// let base = "https://app.krmtool.com/";
let base = "http://localhost:8000/";
const baseUrlApi = `${base}api/`;

const user = window.$('#pk').data('pk');

const configService = {
  apiGetProcesses: `${baseUrlApi}process/`,
  apiGetRisks: `${baseUrlApi}risks/`,
  apiGetDomainRisks: `${baseUrlApi}domain-risks/`,
  apiGetControls: `${baseUrlApi}controls/`,
  apiGetCompanies: `${baseUrlApi}companies?user=${user}`,
  apiGetRiskCompany: `${baseUrlApi}riskscompany/`,
  apiSendRiskTestInherent: `${baseUrlApi}risktestinherentexpert/`,
};

export default configService;
