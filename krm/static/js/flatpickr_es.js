(function (global, factory) {

    if (typeof exports === 'object' && typeof module !== 'undefined') {
        factory(exports)
    }
    else if (typeof define === 'function' && define.amd) {
        define(['exports'], factory)

    } else {
        if ( typeof globalThis !== 'undefined') {
            global = globalThis;
        } else {
            global = global || self, factory(global.es = {});
        }
    }
}(this, (function (exports) { 'use strict';

    var fp;
    if (typeof window !== "undefined" && window.flatpickr) {
        fp = window.flatpickr;
    } else {
        fp = {
            l10ns: {},
        };
    }
  var Spanish = {
      weekdays: {
          shorthand: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
          longhand: [
              "Domingo",
              "Lunes",
              "Martes",
              "Miércoles",
              "Jueves",
              "Viernes",
              "Sábado",
          ],
      },
      months: {
          shorthand: [
              "Ene",
              "Feb",
              "Mar",
              "Abr",
              "May",
              "Jun",
              "Jul",
              "Ago",
              "Sep",
              "Oct",
              "Nov",
              "Dic",
          ],
          longhand: [
              "Enero",
              "Febrero",
              "Marzo",
              "Abril",
              "Mayo",
              "Junio",
              "Julio",
              "Agosto",
              "Septiembre",
              "Octubre",
              "Noviembre",
              "Diciembre",
          ],
      },
      ordinal: function () {
          return "º";
      },
      firstDayOfWeek: 1,
      rangeSeparator: " a ",
      time_24hr: true,
  };
  fp.l10ns.es = Spanish;
  var es = fp.l10ns;

  exports.Spanish = Spanish;
  exports.default = es;

  Object.defineProperty(exports, '__esModule', { value: true });

})));
