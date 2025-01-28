'use strict';

var langEs = {
  processing: 'Procesando...',
  lengthMenu: 'Mostrar _MENU_ registros',
  zeroRecords: 'No se encontraron resultados',
  emptyTable: 'Ningún dato disponible en esta tabla',
  info: 'Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
  infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
  infoFiltered: '(filtrado de un total de _MAX_ registros)',
  infoPostFix: '',
  search: 'Buscar:',
  url: '',
  infoThousands: ',',
  loadingRecords: 'Cargando...',
  oPaginate: {
    First: 'Primero',
    Last: 'Último',
    Next: 'Siguiente',
    Previous: 'Anterior'
  },
  oAria: {
    SortAscending: ': Activar para ordenar la columna de manera ascendente',
    SortDescending: ': Activar para ordenar la columna de manera descendente'
  }
};

var langEn = {
  emptyTable: 'No data available in table',
  info: 'Showing _START_ to _END_ of _TOTAL_ entries',
  infoEmpty: 'Showing 0 to 0 of 0 entries',
  infoFiltered: '(filtered from _MAX_ total entries)',
  infoPostFix: '',
  infoThousands: ',',
  lengthMenu: 'Show _MENU_ entries',
  loadingRecords: 'Loading...',
  processing: 'Processing...',
  search: 'Search:',
  zeroRecords: 'No matching records found',
  oPaginate: {
    First: 'First',
    Last: 'Last',
    Next: 'Next',
    Previous: 'Previous'
  },
  oAria: {
    SortAscending: ': activate to sort column ascending',
    SortDescending: ': activate to sort column descending'
  }
};

var CustomDatatables = {
  init: function () {
    let table = $('.customDatatable');
    let langSelected = langEs;
    let url = window.location.pathname;
    if (url.indexOf('/en/') != -1) {
      langSelected = langEn;
    }

    // begin first table
    table.DataTable({
      responsive: true,
      lengthMenu: [5, 10, 25, 50],
      pageLength: 10,
      language: langSelected,
      "dom":
        "<'row'" +
        "<'col-sm-6 d-flex align-items-center justify-conten-start'l>" +
        "<'col-sm-6 d-flex align-items-center justify-content-end'f>" +
        ">" +
        "<'table-responsive'tr>" +
        "<'row'" +
        "<'col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start'i>" +
        "<'col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end'p>" +
        ">"
    });
  },

  destroy: function () {
    $('.customDatatable').DataTable().destroy();
    if($('#riskkrc').length) {
      $('#riskkrc').DataTable().destroy();
    }
  },

  initEvalKrc: function () {
    let table = $('#riskkrc');
    let langSelected = langEs;
    let url = window.location.pathname;
    if (url.indexOf('/en/') != -1) {
      langSelected = langEn;
    }

    // begin first table
    table.DataTable({
      responsive: true,
      lengthMenu: [5, 10, 25, 50],
      pageLength: 10,
      columnDefs: [
        {
            targets: [0], // Índice de la columna donde deseas desactivar la ordenación
            orderable: false
        }
      ],
      order: [[1, 'asc']],
      language: langSelected,
      "dom":
        "<'row'" +
        "<'col-sm-6 d-flex align-items-center justify-conten-start'l>" +
        "<'col-sm-6 d-flex align-items-center justify-content-end'f>" +
        ">" +
        "<'table-responsive'tr>" +
        "<'row'" +
        "<'col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start'i>" +
        "<'col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end'p>" +
        ">"
    });
  },


  initEvalRR: function () {
    let table = $('#riskrr');
    let langSelected = langEs;
    let url = window.location.pathname;
    if (url.indexOf('/en/') != -1) {
      langSelected = langEn;
    }

    // begin first table
    table.DataTable({
      responsive: true,
      lengthMenu: [5, 10, 25, 50],
      pageLength: 10,
      language: langSelected,
      "dom":
        "<'row'" +
        "<'col-sm-6 d-flex align-items-center justify-conten-start'l>" +
        "<'col-sm-6 d-flex align-items-center justify-content-end'f>" +
        ">" +
        "<'table-responsive'tr>" +
        "<'row'" +
        "<'col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start'i>" +
        "<'col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end'p>" +
        ">"
    });
  },

  initEvalRI: function () {
    let table = $('#riskri');
    let langSelected = langEs;
    let url = window.location.pathname;
    if (url.indexOf('/en/') != -1) {
      langSelected = langEn;
    }

    // begin first table
    table.DataTable({
      responsive: true,
      lengthMenu: [5, 10, 25, 50],
      pageLength: 10,
      language: langSelected,
      "dom":
        "<'row'" +
        "<'col-sm-6 d-flex align-items-center justify-conten-start'l>" +
        "<'col-sm-6 d-flex align-items-center justify-content-end'f>" +
        ">" +
        "<'table-responsive'tr>" +
        "<'row'" +
        "<'col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start'i>" +
        "<'col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end'p>" +
        ">"
    });
  },

  initEvalCompanies: function () {
    let table = $('#evalcompanies');
    let langSelected = langEs;
    let url = window.location.pathname;
    if (url.indexOf('/en/') != -1) {
      langSelected = langEn;
    }

    // begin first table
    table.DataTable({
      responsive: true,
      lengthMenu: [5, 10, 25, 50],
      pageLength: 10,
      language: langSelected,
      "dom":
        "<'row'" +
        "<'col-sm-6 d-flex align-items-center justify-conten-start'l>" +
        "<'col-sm-6 d-flex align-items-center justify-content-end'f>" +
        ">" +
        "<'table-responsive'tr>" +
        "<'row'" +
        "<'col-sm-12 col-md-5 d-flex align-items-center justify-content-center justify-content-md-start'i>" +
        "<'col-sm-12 col-md-7 d-flex align-items-center justify-content-center justify-content-md-end'p>" +
        ">"
    });
  },

};

$(document).ready(function () {
  CustomDatatables.init();
});
