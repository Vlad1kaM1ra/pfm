function validateForm() {
    var email = document.forms["login"]["email"].value;
    var password = document.forms["login"]["password"].value;
    var errorMessage = document.getElementsByClassName("error").item(0)
    if (email == "" || password == "") {
        errorMessage.innerText = "Login and password must be provided";
        return false;
    }
    return true;
}

function getCurrentDate() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    }

    var currentDate = dd + '/' + mm + '/' + yyyy;

    document.getElementById("currentDate").innerHTML = currentDate;
}

function setExpenditure() {
    var expenditureItems = document.getElementsByClassName("justify-content-between lh-condensed");
    var len = expenditureItems.length;
    for (i = 0; i < len; i++) {
        expenditureItems
            .item(i)
            .getElementsByClassName("text-muted")
            .item(0)
            .innerHTML = Math.floor(Math.random() * 100) + "&euro;";
    }
}

function setTotal() {
    var expenditureItems = document.getElementsByClassName("justify-content-between lh-condensed");
    var len = expenditureItems.length;
    var total = 0;
    for (i = 0; i < len; i++) {
        total += parseInt(expenditureItems
            .item(i)
            .getElementsByClassName("text-muted")
            .item(0)
            .innerHTML)
    }
    document.getElementsByClassName("list-group-item d-flex justify-content-between text-success")
        .item(0)
        .getElementsByTagName("strong")
        .item(1)
        .innerHTML = total + "&euro;"

}

function mainInit() {
    getCurrentDate();
    setExpenditure();
    setTotal();
}

$(function () {
    $('#datepicker').datepicker({
        onSelect: function (dateText) {
            $('#datepicker2').datepicker("setDate", $(this).datepicker("getDate"));
            setDate($(this).datepicker("option", "dateFormat", "dd-mm-yy").val());
        }
    });
});

$(function () {
    $("#datepicker2").datepicker();
});

function setDate(date) {
    var dates = document.getElementsByName("date");
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
    params = getUrlParams(urlparams);
    document.getElementById("getData").innerHTML =
        params["category"] + " on " + params["date"];

}

var counter = 0;

function moreFields() {
    counter++;
    var newFields = document.getElementById('readroot').cloneNode(true);
    newFields.id = '';
    newFields.style.display = 'block';
    var newField = newFields.getElementsByTagName("input")
    for (var i = 0; i < newField.length; i++) {
        var theName = newField[i].name
        var theValue = newField[i].value
        if (theName)
            newField[i].name = theName + counter;
        if (theValue)
            newField[i].value = "";
    }
    var insertHere = document.getElementById('writeroot');
    insertHere.parentNode.insertBefore(newFields, insertHere);
}

function callTotal(){
    moreFields();
}

