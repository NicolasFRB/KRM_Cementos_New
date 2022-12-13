import React from "react";
// import { useState, useEffect } from "react";
import Select from 'react-select'
// import { useTranslation } from "react-i18next";

function SelectScopes({ scopes, setScopesSelected }) {

  return (
    <div>
      <div className="col col-12 col-sm-6">
        <h5>Alcances</h5>
        <Select options={scopes} isMulti onChange={(scopes) => setScopesSelected(scopes)} />
      </div>
    </div>
  );
}

export default SelectScopes;
