import configService from "../services/config.js";
import React from "react";
import { useState, useEffect } from "react";
import Select from 'react-select'

function SelectQuestionnaire({ questionnaire, setQuestionnaire, selectedQuestions, setSelectedQuestions }) {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    // const [questionnaires, setQuestionnaires] = useState([]);
    const [selectOptions, setSelectOptions] = useState([]);

    useEffect(() => {
        fetch(configService.apiGetQuestionnaires)
            .then((res) => res.json())
            .then(
                (res) => {
                    // setQuestionnaires(res.results);
                    let newSelectOptions = res.results.map((questionnaire) => {
                        return {
                            value: questionnaire.pk,
                            label: questionnaire.name
                        }
                    });
                    newSelectOptions.unshift({ value: 0, label: '-' });
                    setSelectOptions(newSelectOptions);
                    setIsLoaded(true);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            );
    }, []);

    if (error) {
        return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Cargando cuestionarios...</div>;
    } else {
        return (
            <div>
                {isLoaded && selectOptions && (
                    <div className="col col-12 col-md-6" key={questionnaire}>
                        <Select options={selectOptions} defaultValue={selectOptions[0]} onChange={setQuestionnaire} selectedQuestions={selectedQuestions} setSelectedQuestions={setSelectedQuestions} />
                        <input type="hidden" name="questionnaire" value={questionnaire.value} />
                    </div>
                )}
            </div>
        );
    }
}

export default SelectQuestionnaire;
