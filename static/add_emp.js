$(document).ready(function() {
            $("#add-employee").click(function (){
                $('.ui.modal').modal('show');
                })
            $("#save_emp").click(function(){
                    var inputs = document.querySelectorAll(".form input")
                    var inputs_len = inputs.length
                    var post_data = {}
                    for (var i=0; i < inputs_len; i++){
                        if (inputs[i].id === "salary"){
                            post_data[inputs[i].id] = parseFloat(inputs[i].value)
                        }
                        else {
                            post_data[inputs[i].id] = inputs[i].value
                        }
                    }
                    var gender = document.getElementById("gender")
                    post_data[gender.id] = gender.value
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