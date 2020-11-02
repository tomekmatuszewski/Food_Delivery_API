function addClient() {
    $("#new-client").modal('show');
}

function saveClient() {
    var inputs = document.querySelectorAll("#new-client .form input")
    var inputs_len = inputs.length
    const post_data = {}
    for (var i=0; i < inputs_len; i++){
        post_data[inputs[i].className] = inputs[i].value
    }
    $.ajax({
        url: window.location.href,
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        dataType: 'json'
    });
    $("#new-client").modal('hide');
}

function updateClient(element){
    var tr = element.parentNode.parentNode.children;
    var client_inputs = document.querySelectorAll("#edit-client .form input");

    for (let i=0; i < client_inputs.length; i++){
        client_inputs[i].value = tr[i+1].textContent;
    }
    idToform = document.querySelector("#edit-client span")
    idToform.innerHTML = tr[0].textContent

    $("#edit-client").modal('show');
}

function saveUpdatedClient(){
    var client_inputs = document.querySelectorAll("#edit-client .form input");
    var post_data = {}
    for (let i=0; i < client_inputs.length; i++){
        post_data[client_inputs[i].className] = client_inputs[i].value
    }
    id = document.querySelector("#edit-client span").innerHTML
    $.ajax({
        url: window.location.href + "/" + id + "/update",
        type: "PUT",
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        dataType: 'json'
    });
    $("#edit-client").modal('hide');
}

function deleteClient(element){
    var idToform = element.parentNode.parentNode.children[0].textContent;
    id = document.querySelector("#delete-client .content span")
    id.innerHTML = idToform
    $('#delete-client').modal('show');
}

function deleteClientConfirm (){
    id = document.querySelector("#delete-client .content span").innerHTML
    $.ajax({
        url: window.location.href + "/" + id + "/delete",
        type: "DELETE",
        contentType: 'application/json',
        dataType: 'json'
    });
    $("#delete-client").modal('hide');
}


