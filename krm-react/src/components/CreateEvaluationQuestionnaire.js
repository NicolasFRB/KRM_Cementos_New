import React from "react";
import { useState, useEffect } from "react";

import SelectQuestionnaire from "./SelectQuestionnaire.js";
import SelectQuestions from "./SelectQuestions.js";

let $ = window.$;

function CreateEvaluationKrmInherent(props) {
    const [formData, setFormData] = useState({ 'completed': false });
    const [questionnaire, setQuestionnaire] = useState({ value: 0, label: '-' });
    const [selectedQuestions, setSelectedQuestions] = useState([]);

    const readFormData = () => {
        let newFormData = {};
        newFormData.ref = $('#e_ref').val();
        newFormData.date_begin = $('#e_date_begin').val();
        newFormData.date_end = $('#e_date_end').val();
        newFormData.description = $('#e_description').val();
        newFormData.completed = newFormData.ref !== '' && newFormData.date_begin !== '' && newFormData.date_intermediate !== '' && newFormData.date_end !== '';
        setFormData(newFormData);
    }

    useEffect(() => {
        $('#e_ref, #e_date_begin, #e_date_intermediate, #e_date_end, #e_description').on('change', readFormData);
        // eslint-disable-next-line
    }, []);

    // useEffect(() => {
    //     window.CustomDatatables.destroy();
    //     window.CustomDatatables.init();
    // }, []);

    const sendForm = (e) => {
        e.preventDefault();
        if (formData.completed === false) {
            alert('Falta algún dato imprescindible en el formulario');
            return false;
        }

        $(e.currentTarget).attr('data-kt-indicator', 'on');
        document.getElementById("evaluation_questionnaire_create").submit();
    }

    return (
        <div className="App">
            <div className="row">
                <div className="col-12">
                    <h3 className="mb-6">Paso 2: Seleccione el cuestionario a evaluar</h3>
                    {formData.completed === false && (
                        <div className="alert alert-primary">Complete todos los datos obligatorios sobre la evaluación</div>
                    )}
                    <div className={(formData.completed ? '' : 'd-none')}>
                        <SelectQuestionnaire questionnaire={questionnaire} setQuestionnaire={setQuestionnaire} />
                    </div>
                    <div className="separator my-10"></div>
                </div>
                <div className="col-12">
                    <h3 className="mb-5">Paso 3: Seleccione las preguntas a evaluar y los usuarios evaluadores</h3>
                    {questionnaire.value !== 0 ? (
                        <SelectQuestions questionnaire={questionnaire} selectedQuestions={selectedQuestions} setSelectedQuestions={setSelectedQuestions} />
                    ) : (
                        <div className="alert alert-primary">Selecciona el cuestionario para poder mostrar las preguntas asociadas</div>
                    )}
                </div>

                <div className="separator my-10"></div>
                <div className="col-12" id="launch">
                    <h3 className="mb-5">Paso 4: Resumen y lanzamiento</h3>
                    {selectedQuestions.length === 0 ? (
                        <div className="alert alert-primary">Selecciona al menos una pregunta para poder lanzar la evaluación</div>
                    ) : (
                        <div className="col-12">
                            <p>Se van a lanzar en total {selectedQuestions.length} preguntas </p>
                            <button onClick={sendForm} type="button" className="btn btn-primary btn-sm px-6 align-self-center text-nowrap" data-kt-indicator="off">
                                <span className="indicator-label">Lanzar evaluaciones</span>
                                <span className="indicator-progress">
                                    Lanzando...<span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                                </span>
                            </button>
                            <input type="hidden" name="questions_to_evaluate" value={JSON.stringify(selectedQuestions.map((question) => {
                                return {
                                    pk: question.pk,
                                    evaluators: question.evaluators.map((evaluator) => {
                                        return evaluator.value
                                    })
                                };
                            }))} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default CreateEvaluationKrmInherent;
