function addOrder() {
    $("#new-order").modal('show');
}

function saveOrder() {
    var inputs = document.querySelectorAll("#new-order .form input, #new-order .form select, #new-order .form textarea");
    var post_data = {}
    for (var i=0; i < inputs.length; i++){
        if (inputs[i].tagName === "SELECT"){
            post_data[inputs[i].title] = parseInt(inputs[i].value)
        }
        else if (inputs[i].className === "full_price") {
            post_data[inputs[i].className] = parseFloat(inputs[i].value)
        }
        else{
            post_data[inputs[i].className] = inputs[i].value
        }
    }
    $.ajax({
        url: window.location.href,
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        dataType: 'json'
    });
    $('#new-order').modal('hide');
}

function updateOrder(element){
    var tr = element.parentNode.parentNode.children;
    var user_tr = [];
    for (let i=0; i < tr.length; i++){
        if (tr[i].className === "user-input" || tr[i].className === "user-select"){
            user_tr.push(tr[i])
        }
    }
    var inputs = document.querySelectorAll("#edit-order .form input, #edit-order .form select, #edit-order .form textarea");

    for (let i=0; i < inputs.length; i++){
        if (user_tr[i].className === "user-select"){
            inputs[i].value = user_tr[i].title
        }
        else {
             inputs[i].value = user_tr[i].textContent
        }
    }

    idToform = document.querySelector("#edit-order span");
    idToform.innerHTML = tr[0].textContent;

    $("#edit-order").modal('show');
}

function saveUpdatedOrder(){
    var inputs = document.querySelectorAll("#edit-order .form input, #edit-order .form select, #edit-order .form textarea")
    var post_data = {}
     for (var i=0; i < inputs.length; i++){
        if (inputs[i].tagName === "SELECT"){
            post_data[inputs[i].title] = parseInt(inputs[i].value)
        }
        else if (inputs[i].className === "full_price") {
            post_data[inputs[i].className] = parseFloat(inputs[i].value)
        }
        else{
            post_data[inputs[i].className] = inputs[i].value
        }
    }
    id = document.querySelector("#edit-order span").innerHTML
    $.ajax({
        url: window.location.href + "/" + id + "/update",
        type: "PUT",
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        dataType: 'json'
    });
    $('#edit-order').modal('hide');
}


function deleteOrder(element){
    var idToform = element.parentNode.parentNode.children[0].textContent;
    id = document.querySelector("#delete-order .content span")
    id.innerHTML = idToform
    $('#delete-order').modal('show');
}

function deleteOrderConfirm () {
    id = document.querySelector("#delete-order .content span").innerHTML
    $.ajax({
        url: window.location.href + "/" + id + "/delete",
        type: "DELETE",
        contentType: 'application/json',
        dataType: 'json'
    });
    $("#delete-order").modal('hide');
}