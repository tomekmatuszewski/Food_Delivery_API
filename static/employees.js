function addEmployee() {
    $('#new-employee').modal('show');
}

function saveEmployee() {
    var inputs = document.querySelectorAll("#new-employee .form input")
    var post_data = {}
    for (var i=0; i < inputs.length; i++){
        if (inputs[i].className === "salary"){
            post_data[inputs[i].className] = parseFloat(inputs[i].value)
        }
        else {
            post_data[inputs[i].className] = inputs[i].value
        }
    }
    var gender = document.querySelector("#new-employee select")
    post_data[gender.title] = gender.value
    $.ajax({
        url: window.location.href,
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        dataType: 'json'
    });
    $('#new-employee').modal('hide');
}

function updateEmployee(element){
    var tr = element.parentNode.parentNode.children;
    var emp_inputs = document.querySelectorAll("#edit-employee .form input, #edit-employee .form select");

    for (let i=0; i < emp_inputs.length; i++){
        emp_inputs[i].value = tr[i+1].textContent;
    }

    idToform = document.querySelector("#edit-employee span");
    idToform.innerHTML = tr[0].textContent;

    $("#edit-employee").modal('show');
}


function saveUpdatedEmployee(){
    var emp_inputs = document.querySelectorAll("#edit-employee .form input, #edit-employee .form select");
    var post_data = {}
    for (let i=0; i < emp_inputs.length; i++){
        if (emp_inputs[i].title !== "" ) {
            post_data[emp_inputs[i].title] = emp_inputs[i].value
        }
        else {
            post_data[emp_inputs[i].className] = emp_inputs[i].value
        }
    }
    id = document.querySelector("#edit-employee span").innerHTML
    $.ajax({
        url: window.location.href + "/" + id + "/update",
        type: "PUT",
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        dataType: 'json'
    });
    $("#edit-employee").modal('hide');
}


function deleteEmployee(element){
    var idToform = element.parentNode.parentNode.children[0].textContent;
    id = document.querySelector("#delete-emp .content span")
    id.innerHTML = idToform
    $('#delete-emp').modal('show');
}

function deleteEmployeeConfirm (){
    id = document.querySelector("#delete-emp .content span").innerHTML
    $.ajax({
        url: window.location.href + "/" + id + "/delete",
        type: "DELETE",
        contentType: 'application/json',
        dataType: 'json'
    });
    $("#delete-emp").modal('hide');
}









