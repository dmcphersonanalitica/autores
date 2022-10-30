$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            timeout: 1000,
            data: {
                'action': 'list'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "fecha_format"},
            {"data": "libro"},
            {"data": "mercado"},
            {"data": "cantidad"},
            {"data": "precio"},
            {"data": "totales"},
            {"data": "options"},
        ],
        columnDefs: [
            {
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    let superadm = window.superadm.args;
                    var buttons = '<a href="/mecs/sales/detail/'+row.idventas+'/" class="btn bg-gradient-success btn-xs" style="width: 25px" title="Ver detalles de venta"><i class="fas fa-info"></i></a> | ';
                    buttons += '<a href="/mecs/sales/invoice/pdf/'+row.idventas+'/" class="btn bg-gradient-secondary btn-xs" style="width: 25px" title="Descargar reporte de venta"><i class="fas fa-download"></i></a>';
                    if (superadm === 'si')
                        buttons += ' | <a href="/mecs/sales/mail/'+row.idventas+'/" class="btn bg-gradient-info btn-xs" style="width: 25px" title="Enviar reporte de venta"><i class="fas fa-envelope"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [6],
                class: 'text-center',
                render: function (data, type, row){
                    var text = '$' + data;
                    return text
                }
            },
            {
                targets: [5],
                class: 'text-center',
                 render: function (data, type, row){
                    var text = '$' + data;
                    return text
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
        ],
        initComplete: function (settings, json) {
        }
    });
});