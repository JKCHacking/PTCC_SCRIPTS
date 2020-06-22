$(document).ready(function() {
            
    $("#add-employee-button").click(function(){
        $("#addEmployeeModal").modal("dispose");
        $("#addEmployeeModal").modal();
    });

    $("#employee-input-form").submit(function(e){
        e.preventDefault();
        var errorFlag = checkUserInput();
        if (errorFlag !== 1) {
            sendEmployeeDetails($(this));
        }
        $("#addEmployeeModal").modal("hide");
    });

    $("#delete-employee-button").click(function(){
        var html_string;
        var employee_name;

        $("#infoModal").modal();
        $(".info-modal-title").html("Deleting Employees");
        html_string = "<h6>These are the employees that will be deleted: </h6>";
        $.each($('input.form-check-input'), function() {
            if ($(this).prop("checked")) {
                employee_name = $(this).data("empname");
                html_string += "<h6>* <strong>"+ employee_name + "</strong></h6>"
                employeeIdList.push($(this).data("id"));
            }
        });

        if (employeeIdList.length == 0) {
            html_string = "<h6>No selected employees.</h6>"
            $("#delete_button").attr("disabled", true);
        } else {
            $("#delete_button").attr("disabled", false);
        }

        $(".info-modal-body").html(html_string);
        $("#delete_button").attr("hidden", false);
    });

    $("#delete_button").click(function(){
        deleteEmployees();
        $("#delete_button").attr("hidden", true);
    });

    function putErrorMessage(errorTextContainer, inputElement, message) {
        inputElement.addClass("error");
        errorTextContainer.attr("hidden", false);
        errorTextContainer.html(message);
    }

    function checkUserInput() {
        var errorFlag = 0;
        $.each($(".add-input"), function() {
            var inputType = $(this).data("type");
            var userInput = ($(this).val()).trim();
            var group_container = $(this).parent("div");
            var errorElem = group_container.find(".error-text");
            var errorMessageHtml = "";

            errorElem.attr("hidden", true);
            $(this).removeClass("error");
            if (inputType == "format_text") {
                if(userInput == "" || !userInput) {
                    putErrorMessage(errorElem, $(this), "Empty Input");
                    errorFlag = 1;
                }
            } else if (inputType == "format_date") {
                userInput = convertDate(userInput);
                if(userInput.includes("NaN") || !userInput) {
                    putErrorMessage(errorElem, $(this), "Invalid Date");
                    errorFlag = 1;
                }
            } else if (inputType == "format_float") {
                if(userInput == "" || !userInput || isNaN(userInput)) {
                    putErrorMessage(errorElem, $(this), "Input must be numbers, remove dashes or spaces between numbers");
                    errorFlag = 1;
                }
            }
        });
        return errorFlag;
    }

    function convertDate(date_string) {
        var month_shortcuts = {
            "Jan.": "January",
            "Feb.": "February",
            "Aug.": "August",
            "Sept." : "September",
            "Oct." : "October",
            "Nov." : "November",
            "Dec." : "December"
        };
        
        var month = date_string.split(" ")[0];
        if (month.includes(".")) {
            date_string = date_string.replace(month, month_shortcuts[month]);
        }
        var options = { year: 'numeric', month: 'long', day: 'numeric' };
        var date = new Date(date_string);
        var dateString;

        if(isNaN(date_string[0])) {
            dateString = (date.getFullYear() + "-" + ("0" + (date.getMonth()+1)).slice(-2) + "-" + ("0" + date.getDate()).slice(-2));
        } else {
            dateString = date.toLocaleDateString("en-US", options)
        }
        return dateString;
    }

    function deleteEmployees() {
        data = {
            "employeeList": employeeIdList
        };
        $.ajax({
            url:url_delete_employee,
            type:"POST",
            data:data
        })
        .done(function(response) {
            $(".info-modal-title").html(response.head);
            $(".info-modal-body").html(response.body);
            $("#infoModal").modal();
        })
        .fail(function(xhr, status, error) {
            $(".info-modal-title").html("Failed");
            $(".info-modal-body").html("Failed to save <br> data! details: " + (xhr.responseText).split(".")[0]);
            $("#infoModal").modal();
        });
    }

    function sendEmployeeDetails(userFormData) {
        var formData = new FormData();
        var userDataSerialize = userFormData.serializeArray();
        $.each(userDataSerialize, function(key, input){
            formData.append(input.name, input.value);
        });
        
        $.ajax({
            url: url_add_employee,
            data: formData,
            contentType: false,
            processData: false,
            type: 'POST'
        })
        .done(function(response) {
            $(".info-modal-title").html(response.head);
            $(".info-modal-body").html(response.body);
            $("#infoModal").modal();
        })
        .fail(function(xhr, status, error) {
            $(".info-modal-title").html("Failed");
            $(".info-modal-body").html("Failed to save <br> data! details: " + (xhr.responseText).split(".")[0]);
            $("#infoModal").modal();
        });
    }
});