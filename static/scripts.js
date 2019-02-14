function validateLogin() {
    let email = document.forms["login"]["email"].value;
    let password = document.forms["login"]["password"].value;
    let errorMessage = document.getElementsByClassName("error").item(0)
    if (email == "" || password == "") {
        errorMessage.innerText = "Login and password must be provided";
        return false;
    } else {
        let response = httpGet(
            "/check_credentials?email=" + email
            + "&password=" + password)
            .toString().trim();
        if (response == "false") {
            errorMessage.innerText = "Invalid email and/or password";
            return false;
        }
    }
    return true;
}

function httpGet(theUrl) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function validateSignUp() {
    let email = document.forms["signup"]["email"].value;
    let password = document.forms["signup"]["password"].value;
    let passwordConfirmation = document.forms["signup"]["confirmation"].value;
    let errorMessage = document.getElementsByClassName("error").item(0);
    if (email == "" || password == "" || passwordConfirmation == "") {
        errorMessage.innerText = "Login, password and password must be provided";
        return false;
    } else if (password != passwordConfirmation) {
        errorMessage.innerText = "Password and confirmation not match";
        return false;
    } else {
        let response = httpGet("/check_user?email=" + email).toString().trim();
        if (response == "true") {
            errorMessage.innerText = email + " already exists in base!";
            return false;
        }
    }
    return true;
}

function getCurrentDate() {
    let today = new Date();
    let dd = today.getDate();
    let mm = today.getMonth() + 1; //January is 0!
    let yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    }

    let currentDate = yyyy + '-' + mm + '-' + dd;

    return currentDate;
}

function setSummaryDate(){
    let currentDate = getCurrentDate();

    let currentDateDiv = document.getElementById("currentDate");

    if (currentDateDiv != null) {
        currentDateDiv.innerHTML = currentDate;
    }
}

function checkDateOnExpdeditureMainForm() {
     let date = document.getElementsByName("date").item(0);
     if (date.value == "") {
         setDate(getCurrentDate())
     }
     return true;
}

// function setExpenditure() {
//     let expenditureItems = document.getElementsByClassName("justify-content-between lh-condensed");
//     let len = expenditureItems.length;
//     for (i = 0; i < len; i++) {
//         expenditureItems
//             .item(i)
//             .getElementsByClassName("text-muted")
//             .item(0)
//             .innerHTML = Math.floor(Math.random() * 100) + "&euro;";
//     }
// }
//
// function setTotal() {
//     let expenditureItems = document.getElementsByClassName("justify-content-between lh-condensed");
//     let len = expenditureItems.length;
//     let total = 0;
//     for (i = 0; i < len; i++) {
//         total += parseInt(expenditureItems
//             .item(i)
//             .getElementsByClassName("text-muted")
//             .item(0)
//             .innerHTML)
//     }
//     document.getElementsByClassName("list-group-item d-flex justify-content-between text-success")
//         .item(0)
//         .getElementsByTagName("strong")
//         .item(1)
//         .innerHTML = total + "&euro;"
//
// }
//
// function mainInit() {
//     getCurrentDate();
//     setExpenditure();
//     setTotal();
// }

$(function () {
    $('#datepicker').datepicker({
        onSelect: function (dateText) {
            $('#datepicker2').datepicker("setDate", $(this).datepicker("getDate"));
            setDate($(this).datepicker("option", "dateFormat", "yy-mm-dd").val());
        }
    });
});

$(function () {
    $("#datepicker2").datepicker();
});

function setDate(date) {
    let dates = document.getElementsByName("date");
    for (let i = 0; i < dates.length; i++) {
        dates.item(i).value = date;
    }
}

function getUrlParams(search) {
    let hashes = search.slice(search.indexOf('?') + 1).split('&')
    let params = {}
    hashes.map(hash => {
        let [key, val] = hash.split('=')
        params[key] = decodeURIComponent(val)
    })

    return params
}

function inputCatInit(urlparams) {
    let params = getUrlParams(urlparams);
    document.getElementById("getData").innerHTML =
        params["category"] + " on " + params["date"];
    document.getElementById("category").value = params["category"];
    document.getElementById("date").value = params["date"];
}

function commonInit(params) {
    setSummaryDate();
    inputCatInit(params);
}

var counter = 0;

function moreFields() {
    counter++;
    let newFields = document.getElementById('readroot').cloneNode(true);
    newFields.id = '';
    newFields.style.display = 'block';
    let newField = newFields.getElementsByTagName("input")
    for (var i = 0; i < newField.length; i++) {
        var theValue = newField[i].value
        if (theValue)
            newField[i].value = "";
    }
    var insertHere = document.getElementById('writeroot');
    insertHere.parentNode.insertBefore(newFields, insertHere);
}

function callTotal() {
    moreFields();
}

