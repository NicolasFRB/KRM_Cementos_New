import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectDomainRiskKrmInherent({ selectedDomainRisks, setSelectedDomainRisks, selectedCompanies }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [domainRisks, setDomainRisks] = useState([]);

  const handleOnChange = (pk) => {
    if (selectedDomainRisks.includes(pk)) {
      setSelectedDomainRisks(selectedDomainRisks.filter(item => item !== pk));
    } else {
      setSelectedDomainRisks(selectedDomainRisks.concat([pk]));
    }
  };

  const [t] = useTranslation("global");

  useEffect(() => {

    if(!selectedCompanies.length) return;
    const params = {
      company_pks: selectedCompanies,
    };


    var url = new URL(configService.apiGetDomainRisksCompany);
    for (let k in params) {
      url.searchParams.append(k, params[k]);
    }

    fetch(url)
      .then((res) => res.json())
      .then(
        (res) => {

          let domainRisksSet = [];
          res.filter(r => r).forEach((r) => {
            r.domain_risks.forEach( domainRisk => {
              if (!domainRisksSet.find(dr => dr.pk === domainRisk.pk)) {
                domainRisksSet.push(domainRisk)
              }
            })
          })

          console.log("Domain risks from company", Array.from(domainRisksSet));
          setDomainRisks(Array.from(domainRisksSet));
          setIsLoaded(true);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
  }, [selectedCompanies]);



  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>{t('risks.loading-domain-risks')}...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <h5 className="mb-6">{t('risks.select-domain-risk')}</h5>
            {domainRisks.map((value, index) => {
              return <p key={value.pk}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value.pk)} className="form-check-input" name="process" type="checkbox" value={value.pk} />
                  <span className="fw-semibold ps-2 fs-6">{value.name}</span>
                </label>
              </p>
            })}
          </>
        )}
      </div>
    );
  }
}

export default SelectDomainRiskKrmInherent;
