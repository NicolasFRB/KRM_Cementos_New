import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

function SelectControlScopes({ selectedScopes, setSelectedScopes }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [scopes, setScopes] = useState([]);

  let url = configService.apiGetScopes;
  if (window.location.pathname.includes("/en/")) {
    url = url.replace("/es/", "/en/");
  }


  const handleOnChange = (value) => {
    if (selectedScopes.includes(value)) {
      setSelectedScopes(selectedScopes.filter(item => item !== value));
    } else {
      setSelectedScopes(selectedScopes.concat([value]));
    }

    console.print("Selected Scopes", selectedScopes);
  };
  const [t] = useTranslation("global");


  useEffect(() => {
      fetch(`${url}`)
        .then((res) => res.json())
        .then(
          (res) => {
            console.log(res);
            let scopes = [];
            res.forEach(choice => {
              scopes.push({
                value: choice[0],
                text: choice[1]
              });
            });
            setScopes(scopes);
            setIsLoaded(true);
          },
          (error) => {
            setIsLoaded(true);
            setError(error);
          }
        );
    }, []);

  // // useEffect(() => {
  // //   fetch(`${configService.apiGetScopes}`)
  // //     .then((res) => res.json())
  // //     .then(
  // //       (res) => {
  // //         console.log("Scopes: ", res.results)
  // //         setScopes(res.results);
  // //         setIsLoaded(true);
  // //       },
  // //       (error) => {
  //   //         setIsLoaded(true);
  //   //         setError(error);
  //   //       }
  //   //     );
  //   // }, []);
    
  // useEffect(() => {
  //   setScopes([ 
  //     { pk:"G", name:"Group" }, 
  //     { pk:"P", name:"Plant"}
  //   ]);
  //   // setScopes([ 
  //   //   {value:"Group", label:"Group" },
  //   //   {value:"Plant", label:"Plant" },
  //   // ])
  //   setIsLoaded(true);

  // }, []);


  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return <div>{t('controls.loading-controls')}...</div>;
  } else {
    return (
      <div>
        {isLoaded && (
          <>
            <h5 className="mb-6">{t('general.loading-scope')}</h5>
            {scopes.map((value, index) => {
              return <p key={value.value}>
                <label className="form-check form-check-inline form-check-solid me-5">
                  <input onChange={() => handleOnChange(value.value)} className="form-check-input" name="scope" type="checkbox" value={value.value} />
                  <span className="fw-semibold ps-2 fs-6">{value.text}</span>
                </label>
              </p>
            })}
          </>
        )}
      </div>
    );
  }
}

export default SelectControlScopes;
