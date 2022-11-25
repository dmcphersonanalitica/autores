$(function () {
    let superadm = window.superadm.args;
    if (superadm === 'si')
        $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'list'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "fecha"},
            {"data": "titulo"},
            {"data": "autor"},
            {"data": "enviado"},
            {"data": "options"},
        ],
        columnDefs: [
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="/mecs/reports/invoice/pdf/'+row.id+'/" class="btn bg-gradient-secondary btn-xs" style="width: 25px" title="Descargar reporte de venta"><i class="fas fa-download"></i></a>';
                    buttons += ' | <a href="/mecs/reports/mail/'+row.id+'/" class="btn bg-gradient-info btn-xs" style="width: 25px" title="Enviar reporte de venta"><i class="fas fa-envelope"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [4],
                class: 'text-center',
                render: function (data, type, row){
                    return data;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row){
                    return data
                }
            },
            {
                targets: [2],
                class: 'text-center',
                 render: function (data, type, row){
                    return data;
                }
            },
            {
                targets: [1],
                class: 'text-center',
                render: function (data, type, row){
                    return data;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
    else
        $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'list'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "fecha"},
            {"data": "titulo"},
            {"data": "autor"},
            {"data": "options"},
        ],
        columnDefs: [
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="/mecs/reports/invoice/pdf/'+row.id+'/" class="btn bg-gradient-secondary btn-xs" style="width: 25px" title="Descargar reporte de venta"><i class="fas fa-download"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row){
                    return data;
                }
            },
            {
                targets: [2],
                class: 'text-center',
                render: function (data, type, row){
                    return data
                }
            },
            {
                targets: [1],
                class: 'text-center',
                 render: function (data, type, row){
                    return data;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});