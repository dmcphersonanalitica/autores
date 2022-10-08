$(function () {
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
            },
            dataSrc: ""
        },
        columns: [
            {"data": "position"},
            {"data": "full_name"},
            {"data": "username"},
            {"data": "date_joined"},
            {"data": "last_login"},
            {"data": "assigned"},
        ],
        columnDefs: [
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row){
                    var buttons = '<a href="/administration/user/edit/'+row.id+'/" class="btn bg-gradient-warning btn-xs" style="width: 25px" title="Editar usuario"><i class="fas fa-edit"></i></a> | ';
                    buttons += '<a href="/administration/user/delete/'+row.id+'/" class="btn bg-gradient-danger btn-xs" style="width: 25px" title="Eliminar usuario"><i class="fas fa-trash"></i></a>';
                    //buttons += '<buttons class="btn bg-gradient-danger btn-xs" id="deleteUser" onclick="Delete('+row.id+')"><i class="fas fa-trash"></i></buttons>';
                    return buttons;
                }
            },
            {
                targets: [4],
                class: 'text-center',
                render: function (data, type, row){
                    return data
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
            {
                targets: [0],
                class: 'text-center',
                render: function (data, type, row){
                   return data
                }
            },
        ],
        initComplete: function (settings, json){

        }
    });
});
