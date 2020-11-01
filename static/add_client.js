$(document).ready(function() {
            $("#add-client").click(function (){
                $('.ui.modal').modal('show');
                })
            $("#save_client").click(function(){
                    var inputs = document.querySelectorAll(".form input")
                    var inputs_len = inputs.length
                    const post_data = {}
                    for (var i=0; i < inputs_len; i++){
                        post_data[inputs[i].id] = inputs[i].value
                    }
                    $.ajax({
                        url: window.location.href,
                        type: "POST",
                        contentType: 'application/json',
                        data: JSON.stringify(post_data),
                        dataType: 'json'
                    });
                    $('.ui.modal').modal('hide');
                })

        });