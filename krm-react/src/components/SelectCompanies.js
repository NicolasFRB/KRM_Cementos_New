import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";

function SelectCompanies({ selectedCompanies, setSelectedCompanies, companies, setCompanies }) {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    const handleOnChange = (pk) => {
        if (selectedCompanies.includes(pk)) {
            setSelectedCompanies(selectedCompanies.filter(item => item !== pk));
        } else {
            setSelectedCompanies(selectedCompanies.concat([pk]));
        }
    };

    const selectAll = () => {
        setSelectedCompanies(companies.map(company => {
            return company.pk;
        }));
    };

    const unSelectAll = () => {
        setSelectedCompanies([]);
    };

    useEffect(() => {
        fetch(`${configService.apiGetCompanies}`)
            .then((res) => res.json())
            .then(
                (res) => {
                    setCompanies(res);
                    setIsLoaded(true);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            );
    }, [setCompanies]);

    useEffect(() => {
        if (companies.length) {
            window.CustomDatatables.initEvalCompanies();
        }
    }, [companies])

    if (error) {
        return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Cargando compañías...</div>;
    } else {
        return (
            <div>
                {isLoaded && (
                    <>
                        <table className="table table-striped customDatatable" id="evalcompanies">
                            <thead>
                                <tr>
                                    <th className="text-center">
                                        <span onClick={() => selectAll()} className="me-5"><i className="bi bi-clipboard-check"></i></span>
                                        <span onClick={() => unSelectAll()}><i className="bi bi-clipboard"></i></span>
                                    </th>
                                    <th className="fw-semibold">NOMBRE</th>
                                    <th className="fw-semibold">VAT</th>
                                </tr>
                            </thead>
                            <tbody>
                                {companies.map((company, index) => {
                                    return <tr key={company.pk}>
                                        <td className="text-center"><input onChange={() => handleOnChange(company.pk)} className="form-check-input" name="process" type="checkbox" value={company.pk} checked={selectedCompanies.includes(company.pk)} /></td>
                                        <td className="fw-semibold"><label>{company.name}</label></td>
                                        <td>{company.vat}</td>
                                    </tr>
                                })}
                            </tbody>
                        </table>
                        <input type="hidden" name="companies" value={selectedCompanies} />
                    </>
                )}
            </div>
        );
    }
}

export default SelectCompanies;
