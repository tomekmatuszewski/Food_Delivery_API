$(document).ready(function() {
            $("#add-employee").click(function (){
                $('.ui.modal').modal('show');
                })
            // $("#save").click(function(){
            //         var employee_id = $("#employee_id").val();
            //         var client_id = $("#client").val();
            //         var dest_address = $("#dest_address").val();
            //         var price = $("#price").val();
            //         var other_info = $("#other_information").val();
            //         var contact_phone = $("#contact_phone").val();
            //         $.ajax({
            //             url: window.location.href,
            //             type: "POST",
            //             contentType: 'application/json',
            //             data: JSON.stringify({
            //                 "employee_id": parseInt(employee_id),
            //                 "client_id": parseInt(client_id),
            //                 "destination_address": dest_address,
            //                 "contact_phone": contact_phone,
            //                 "full_price": parseFloat(price),
            //                 "other_info": other_info
            //             }),
            //             dataType: 'json'
            //         });
            //         $('.ui.modal').modal('hide');
            //     })

        });