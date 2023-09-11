/**
 * Bubbly - Bootstrap 5 Dashboard & CMS Theme v. 1.2.0
 * Homepage:
 * Copyright 2021, Bootstrapious - https://bootstrapious.com
 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {
    // White DataTable

    const dataTable = new simpleDatatables.DataTable("#datatable1", {
        searchable: true,
    });

    const dataTable2 = new simpleDatatables.DataTable("#datatable2", {
        searchable: true,
    });

    const dataTable3 = new simpleDatatables.DataTable("#datatable3", {
        searchable: true,
    });

    const dataTable4 = new simpleDatatables.DataTable("#datatable4", {
        searchable: true,
    });


    function adjustTableColumns() {
        let columns = dataTable.columns();

        if (window.innerWidth > 900) {
            columns.show([2, 3, 4, 5]);
        } else if (window.innerWidth > 600) {
            columns.hide([4, 5]);
            columns.show([2, 3]);
        } else {
            columns.hide([2, 3, 4, 5]);
        }
    }

    function adjustTableColumns2() {
        let columns = dataTable2.columns();

        if (window.innerWidth > 900) {
            columns.show([2, 3, 4, 5]);
        } else if (window.innerWidth > 600) {
            columns.hide([4, 5]);
            columns.show([2, 3]);
        } else {
            columns.hide([2, 3, 4, 5]);
        }
    }

    function adjustTableColumns3() {
        let columns = dataTable3.columns();

        if (window.innerWidth > 900) {
            columns.show([2, 3, 4, 5]);
        } else if (window.innerWidth > 600) {
            columns.hide([4, 5]);
            columns.show([2, 3]);
        } else {
            columns.hide([2, 3, 4, 5]);
        }
    }

    function adjustTableColumns4() {
        let columns = dataTable4.columns();

        if (window.innerWidth > 900) {
            columns.show([2, 3, 4, 5]);
        } else if (window.innerWidth > 600) {
            columns.hide([4, 5]);
            columns.show([2, 3]);
        } else {
            columns.hide([2, 3, 4, 5]);
        }
    }

    function bootstrapizeHeader(dataTable, dataTable2, dataTable3, dataTable4) {
        const tableWrapper = dataTable.table.closest(".dataTable-wrapper");
        const tableWrapper2 = dataTable2.table.closest(".dataTable-wrapper");
        const tableWrapper3 = dataTable3.table.closest(".dataTable-wrapper");
        const tableWrapper4 = dataTable4.table.closest(".dataTable-wrapper");


        const input = tableWrapper.querySelector(".dataTable-input");
        if (input) {
            input.classList.add("form-control", "form-control-sm");
        }

        const dataTableSelect = tableWrapper.querySelector(".dataTable-selector");
        if (dataTableSelect) {
            dataTableSelect.classList.add("form-select", "form-select-sm");
        }

        const dataTableContainer = tableWrapper.querySelector(".dataTable-container");
        if (dataTableContainer) {
            dataTableContainer.classList.add("border-0");
        }

        const input2 = tableWrapper2.querySelector(".dataTable-input");
        if (input2) {
            input2.classList.add("form-control", "form-control-sm");
        }

        const dataTableSelect2 = tableWrapper2.querySelector(".dataTable-selector");
        if (dataTableSelect2) {
            dataTableSelect2.classList.add("form-select", "form-select-sm");
        }

        const dataTableContainer2 = tableWrapper2.querySelector(".dataTable-container");
        if (dataTableContainer2) {
            dataTableContainer2.classList.add("border-0");
        }

        const input3 = tableWrapper3.querySelector(".dataTable-input");
        if (input3) {
            input3.classList.add("form-control", "form-control-sm");
        }

        const dataTableSelect3 = tableWrapper3.querySelector(".dataTable-selector");
        if (dataTableSelect3) {
            dataTableSelect3.classList.add("form-select", "form-select-sm");
        }

        const dataTableContainer3 = tableWrapper3.querySelector(".dataTable-container");
        if (dataTableContainer3) {
            dataTableContainer3.classList.add("border-0");
        }

        const input4 = tableWrapper4.querySelector(".dataTable-input");
        if (input4) {
            input4.classList.add("form-control", "form-control-sm");
        }

        const dataTableSelect4 = tableWrapper4.querySelector(".dataTable-selector");
        if (dataTableSelect4) {
            dataTableSelect4.classList.add("form-select", "form-select-sm");
        }

        const dataTableContainer4 = tableWrtableWrapper4apper3.querySelector(".dataTable-container");
        if (dataTableContainer4) {
            dataTableContainer4.classList.add("border-0");
        }
    }

    adjustTableColumns();
    adjustTableColumns2();
    adjustTableColumns3();
    adjustTableColumns4();

    window.addEventListener("resize", adjustTableColumns);
    window.addEventListener("resize", adjustTableColumns2);
    window.addEventListener("resize", adjustTableColumns3);
    window.addEventListener("resize", adjustTableColumns4);

    dataTable.on("datatable.init", function () {
        bootstrapizeHeader(dataTable);
    });


    dataTable2.on("datatable.init", function () {
        bootstrapizeHeader(dataTable2);
    });

    dataTable3.on("datatable.init", function () {
        bootstrapizeHeader(dataTable3);
    });

    dataTable4.on("datatable.init", function () {
        bootstrapizeHeader(dataTable4);
    });
});
