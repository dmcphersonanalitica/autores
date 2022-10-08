function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left">';
        $.each(obj, function (key, value) {
            html += '<li>' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    $.confirm({
        theme: 'material',
        title: 'MECS-Error',
        icon: 'fa fa-ban',
        content: html,
        columnClass: 'medium',
        type: 'red',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-danger',
                action: function () {
                }
            }
        }
    });
}

function submit_with_ajax(url, parameters, act, callback) {
    var classButton = 'btn-primary';
    var typeDialog = 'blue';
    if (act === 'add') {
        classButton = 'btn-primary';
        typeDialog = 'blue';
    } else {
        classButton = 'btn-warning';
        typeDialog = 'yellow';
    }
    $.confirm({
        theme: 'material',
        title: 'MECS-Información',
        icon: 'fa fa-info-circle',
        content: '¿Esta seguro de la operación ha realizar?',
        columnClass: 'small',
        type: 'red',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: classButton,
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback();
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {
                        console.log(data);
                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-secondary',
                action: function () {

                }
            }
        }
    });
}
