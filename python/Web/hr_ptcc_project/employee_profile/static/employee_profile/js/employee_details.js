$(document).ready(function() {
    // initialize tables and selection year
    initialize();

    $(document).on("dblclick", ".editable-employee", function() {
       var value = ($(this).text()).trim();
       var data_type = $(this).data("type");
       var name_element = $(this).attr("name");
       var input = "";

       if (name_element == "format_date") {
            value = convertDate(value);
            input = "<input type='date'" + 
                   "class='input-data-employee'" + 
                   "value='"+value+"'>";
       } else if(name_element == "format_select") {
            if (data_type == "employee_status") {
                    input = "<select class='input-data-employee'>" +
                                "<option>"+value+"</option>" +
                                "<option value='P'>P</option>" +
                                "<option value='R1'>R1</option>" +
                                "<option value='R'>R</option>" +
                            "</select>";
            } 
       }

       $(this).html(input);
       $("#save_employee").attr("disabled", false);
    });

    $(document).on("blur", ".input-data-employee", function(){
        var input_values_dict = enterInput2($(this));
        model_changes_dict["edit"].push(input_values_dict);
    });

    $(document).on("keypress", ".input-data-employee", function(e) {
        var key = e.which;

        if (key == 13) {
            var input_values_dict = enterInput2($(this));
            model_changes_dict["edit"].push(input_values_dict);
        }
    });
    
    $("#save_employee").click(function() {
        $("#saveModal").modal();
        message = "You made the following changes: <br>";
        total_edit = model_changes_dict["edit"].length;
        total_delete = model_changes_dict["delete"].length;
        total_add = model_changes_dict["add"].length;

        if (total_edit > 0) {
            message += "Edited " + total_edit + " item(s)<br>";
        }
        if (total_delete > 0) {
            message += "Deleted " + total_delete + " item(s)<br>";
        }
        if (total_add > 0) {
            message += "Added " + total_add + " item(s)<br>";
        }

        message += "<br>Are you sure you want to add the changes?";

        $("#save_button_modal").attr("disabled", false);
        if (!total_add && !total_edit && !total_delete) {
            message = "You have not made any changes<br>";
            $("#save_button_modal").attr("disabled", true);
        }
        
        $(".save-modal-body").html(message);
    });

    $("#save_button_modal").click(function() {
        sendToServer(model_changes_dict);
        $("#save_employee").attr("disabled", true);
        $("#saveModal").modal("hide");
    });

    $("#info_button_close").click(function() {
        $("#infoModal").modal("hide");
        location.reload(true);
    });

    $("#save_button_close").click(function() {
        location.reload(true);
        $("#saveModal").modal("hide");
    });

    $("#employee-details-year-selection").on("change", function(){
        // remove all elements with class "removable"
        $(".removable").remove();
        $('[data-toggle="tooltip"]').tooltip()
        displayEarnedLeave();
        displayLeavesTaken();
        displayOffenses();
    });
    
    //action add button
    $("body").on('click', '.add', function() {
        $("#save_employee").attr("disabled", false);
        var cell_container = $(this).parent("td");
        var row_container = cell_container.parent("tr");
        var edit_element = cell_container.find(".edit");

        //check for error first
        var error_flag = checkInvalidInput(row_container);
        if (error_flag == 0) {
            input_values_dict = enterInput(row_container);
            console.log(input_values_dict["id"]);
            
            if (input_values_dict["id"].includes("new")) {
                model_changes_dict["add"].push(input_values_dict);
            } else {
                model_changes_dict["edit"].push(input_values_dict);
            }
        }
    });

    //action edit button
    $("body").on('click', '.edit', function(){
        console.log("edit button clicked");
        var cell_container = $(this).parent("td");
        var row_container = cell_container.parent("tr");
        var add_element = cell_container.find(".add");
        
        add_element.attr("hidden", false);
        $(this).attr("hidden", true);
        $.each(row_container.find(".editable"), function() {
            var data_type = $(this).data("type");
            var value = ($(this).text()).trim();
            var name_element = $(this).attr("name");
            var input;

            //determine what type of input html to display
            if (name_element == "format_date") {
                    value = convertDate(value);
                    input = "<input type='date'" + 
                            "class='input-data'" + 
                            "value='"+value+"'>";
            } else if(name_element == "format_select") {
                if (data_type == "employee_status") {
                        input = "<select class='input-data'>" +
                                    "<option>"+value+"</option>" +
                                    "<option value='P'>P</option>" +
                                    "<option value='R1'>R1</option>" +
                                    "<option value='R'>R</option>" +
                                "</select>";
                } else if (data_type == "type") {
                        input = "<select class='input-data'>" +
                                    "<option>"+value+"</option>" +
                                    "<option value='SL'>SL</option>" +
                                    "<option value='VL'>VL</option>" +
                                "</select>";
                } else if (data_type == "offense_name") {
                        input = "<select class='input-data'>" +
                                    "<option>"+value+"</option>" +
                                    "<option value='Late'>Late</option>" +
                                    "<option value='No Time-in'>No Time-in</option>" +
                                    "<option value='No Time-out'>No Time-out</option>" +
                                    "<option value='Undertime'>Undertime</option>" +
                                    "<option value='AWOL'>AWOL</option>" +
                                "</select>";
                } 
            }else {
                    input = "<input type='text'" + 
                            "class='input-data'" + 
                            "value='"+value+"'>";
            }
            $(this).html(input);
            $('input[type="text"]')
            // event handler
            .keyup(resizeInput)
            // resize on page load
            .each(resizeInput);
        });
    });

    //action delete button
    $("body").on("click", ".delete", function() {
        $("#save_employee").attr("disabled", false);
        var delete_values_dict = {};
        cell_container = $(this).parent("td");
        row_container = cell_container.parent("tr");
        
        var id = row_container.data("id").toString();
        var table = row_container.data("table");
        delete_values_dict["id"] = id;
        delete_values_dict["table"] = table;
        //check if substring "new" is included in the id string
        if (id.indexOf("new") === -1) {
            model_changes_dict["delete"].push(delete_values_dict);
        } else {
            //remove the new added entry in the model changes container
            var add_changes = model_changes_dict["add"];
            for(var i = 0; i < add_changes.length; i++) {
                if(add_changes[i]["id"] == id){
                    add_changes.splice(i, 1);
                }
            }
        }
        row_container.remove();
    });

    $(".add-new").click(function (){
        table = $(this).data("table");
        if (table == "leaves_taken_table") {
            row_html = "<tr class='removable' data-id='" + employee_id + "-new' data-table='leave'>" +
                        "<td class='editable' data-type='date' name='format_date'></td>" +
                        "<td class='editable' data-type='days' name='format_float' scope='row'></td>" +
                        "<td class='editable' data-type='type' name='format_select' scope='row'></td>" +
                        '<td>'+
                            '<button style="border:none;background:none;" class="add" title="Add" data-toggle="tooltip" hidden="true"><i class="material-icons"></i></button>'+
                            '<button style="border:none;background:none;display:inline-block;" class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                            '<button style="border:none;background:none;" class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                        '</td>'+
                    "</tr>";
            table_class_name = "." + table;
        }
        else if (table == "offenses_table") {
            row_html = "<tr class='removable' data-id='" + employee_id + "-new' data-table='offense'>" +
                            "<td class='editable' data-type='date' name='format_date' scope='row'></td>" +
                            "<td class='editable' data-type='offense_name' name='format_select' scope='row'></td>" +
                            '<td>'+
                                '<button style="border:none;background:none;" class="add" title="Add" data-toggle="tooltip" hidden="true"><i class="material-icons"></i></button>'+
                                '<button style="border:none;background:none;display:inline-block;" class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                                '<button style="border:none;background:none;" class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                            '</td>'+
                        "</tr>";
            table_class_name = "." + table;
        }

        $(table_class_name).append(row_html);
    });

    function initialize() {
        $('[data-toggle="tooltip"]').tooltip()
        populateYearSelection();
        displayEarnedLeave();
        displayLeavesTaken();
        displayOffenses();
    }

    function displayEarnedLeave(){
        var year_selected = $("#employee-details-year-selection option:selected").text();
        var row_html = "";
        var total_vl = parseFloat(employee_prev_vl_bal);
        var total_sl = parseFloat(employee_prev_sl_bal);

        for(var i = 0; i < emp_vl_list.length; i++) {
            var vl_object = emp_vl_list[i];
            var sl_object = emp_sl_list[i];
            var date_string = new Date(vl_object.fields.cut_off).toISOString();
            var date_js = new Date(date_string);
            var leave_year = date_js.getFullYear().toString();
            
            if (leave_year == year_selected) {
                row_html += "<tr class='removable' data-id='" + vl_object.pk + "-" + sl_object.pk + "' data-table='earned'>"+
                                "<th scope='row'>" + date_js.toLocaleDateString("en-US", date_options) + "</th>"+
                                "<td class='editable' data-type='" + vl_object.fields.type + "' name='format_float' scope='row'>" + parseFloat(vl_object.fields.value).toFixed(3) + "</td>"+
                                "<td class='editable' data-type='" + sl_object.fields.type + "' name='format_float' scope='row'>" + parseFloat(sl_object.fields.value).toFixed(3) + "</td>"+
                                '<td>'+
                                    '<button style="border:none;background:none;" class="add" title="Add" data-toggle="tooltip" hidden="true"><i class="material-icons"></i></button>'+
                                    '<button style="border:none;background:none;display:inline-block;" class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                                '</td>'+
                            "</tr>";
                vl_value_str = vl_object.fields.value;
                sl_value_str = sl_object.fields.value;

                total_vl += parseFloat(vl_value_str);
                total_sl += parseFloat(sl_value_str);
            }
        }
        var total_sl_vl_html = "<tr class='removable'>"+
                                    "<th scope='row'>Total</th>" +
                                    "<td>" + total_vl.toFixed(3) +"</td>" +
                                    "<td>" + total_sl.toFixed(3) +"</td>" +
                               "</tr>"
        row_html += total_sl_vl_html;
        $(".earned_leave_table").append(row_html);
    }

    function displayLeavesTaken(){
        var year_selected = $("#employee-details-year-selection option:selected").text();
        var row_html = "";

        for(var i = 0; i < emp_leaves_taken.length; i++) {
            var leave_taken_object = emp_leaves_taken[i];
            var date_string = new Date(leave_taken_object.fields.date).toISOString();
            var date_js = new Date(date_string);
            var leave_year = date_js.getFullYear().toString();

            if (leave_year == year_selected) {
                row_html += "<tr class='removable' data-id='" + leave_taken_object.pk + "' data-table='leave'>" +
                                "<td class='editable' data-type='date' name='format_date'>" + date_js.toLocaleDateString("en-US", date_options) + "</td>" +
                                "<td class='editable' data-type='days' name='format_float' scope='row'>" + parseFloat(leave_taken_object.fields.days).toFixed(2) + "</td>" +
                                "<td class='editable' data-type='type' name='format_select' scope='row'>" + leave_taken_object.fields.type + "</td>" +
                                '<td>'+
                                    '<button style="border:none;background:none;" class="add" title="Add" data-toggle="tooltip" hidden="true"><i class="material-icons"></i></button>'+
                                    '<button style="border:none;background:none;display:inline-block;" class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                                    '<button style="border:none;background:none;" class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                                '</td>'+
                            "</tr>";
            }
        }
        $(".leaves_taken_table").append(row_html);
    }

    function displayOffenses(){
        var year_selected = $("#employee-details-year-selection option:selected").text();
        var row_html = "";

        for(var i = 0; i < emp_offenses.length; i++) {
            var offense_object = emp_offenses[i];
            var date_string = new Date(offense_object.fields.date).toISOString();
            var date_js = new Date(date_string);
            var leave_year = date_js.getFullYear().toString();
            if (leave_year == year_selected) {
                row_html += "<tr class='removable' data-id='" + offense_object.pk + "' data-table='offense'>" +
                                "<td class='editable' data-type='date' name='format_date' scope='row'>"+ date_js.toLocaleDateString("en-US", date_options) +"</td>" +
                                "<td class='editable' data-type='offense_name' name='format_select' scope='row'>" + offense_object.fields.offense_name + "</td>" +
                                '<td>'+
                                    '<button style="border:none;background:none;" class="add" title="Add" data-toggle="tooltip" hidden="true"><i class="material-icons"></i></button>'+
                                    '<button style="border:none;background:none;display:inline-block;" class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                                    '<button style="border:none;background:none;" class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons"></i></button>'+
                                '</td>'+
                            "</tr>";
            }
        }
        $(".offenses_table").append(row_html);
    }

    function populateYearSelection() {
        var start_year = 1999;
        var end_year = new Date().getFullYear();
        var options = "";
        for (var year = end_year; year >= start_year; year-- ) {
            options += "<option value=" + year +">"+ year + "</option>";
        }
        $("#employee-details-year-selection").html(options);
    }

    //function to check for incorrect input in the table cell
    function checkInvalidInput(row_container) {
        var error_flag = 0;
        $.each(row_container.find(".editable"), function() {
            var name_input_element = $(this).attr("name");
            var input_element = $(this).find(".input-data");
            var value = (input_element.val()).trim();
            var year_selected = $("#employee-details-year-selection option:selected").text();

            $(this).removeClass("error");
            if(name_input_element == "format_float") {
                if (isNaN(value) || value === "") {
                    $(this).addClass("error");
                    error_flag = 1;
                }
            } else if(name_input_element == "format_date") {
                var date_js = new Date(value);
                var date_obj = convertDate(value);
                //checking if the chosen year of the date is equal to the year selection
                if (date_obj == "NaN-aN-aN" || date_js.getFullYear().toString() != year_selected) {
                    $(this).addClass("error");
                    error_flag = 1;
                } 
            } else if(name_input_element == "format_select") {
                if (value == "") {
                    $(this).addClass("error");
                    error_flag = 1;
                }
            }
        });
        return error_flag;
    }

    // function serves the add edit and delete of table objects
    function enterInput(row_container) {
        var input_values_dict = {};
        var id = row_container.data("id");
        var table = row_container.data("table");

        input_values_dict["id"] = id;
        input_values_dict["table"] = table;
        $.each(row_container.find(".editable"), function(){
            var type = $(this).data("type");
            var name_input_element = $(this).attr("name");
            var input_element = $(this).find(".input-data");
            var value = (input_element.val()).trim();
            if(name_input_element == "format_date") {
                value = convertDate(value);
            }

            input_values_dict[type] = value;
            input_element.remove();
            $(this).html(value);
        });
        $(".add").attr("hidden", true);
        $(".edit").attr("hidden", false);
        return input_values_dict;
    }

    // this function serves the editing of employee data
    function enterInput2(input_element) {
        var input_values_dict = {};
        var parent_container = input_element.parent("td");
        var id = parent_container.data("id");
        var table = parent_container.data("table");
        var type = parent_container.data("type");
        var type_of_input = parent_container.attr("name");

        var value = (input_element.val()).trim();
        if(type_of_input == "format_date") {
            value = convertDate(value);
        }

        input_element.remove();
        parent_container.html(value);

        input_values_dict["id"] = id;
        input_values_dict["table"] = table;
        input_values_dict[type] = value;

        return input_values_dict;
    }
    function resizeInput() {
        $(this).attr('size', $(this).val().length);
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

    function sendToServer(model_changes_dict) {
        console.log(model_changes_dict);
        data = {
            "model_changes_dict": JSON.stringify(model_changes_dict)
        }
        $.ajax({
            url:url_save_changes,
            type: "POST",
            dataType: "json",
            data: data
        })
        .done(function(response) {
            $(".info-modal-title").html(response.head);
            $(".info-modal-body").html(response.body);
            $("#infoModal").modal();
            model_changes_dict = {
                "edit":[],
                "delete":[]
            };
        })
        .fail(function(xhr, status, error) {
            $(".info-modal-title").html("Failed");
            $(".info-modal-body").html("Failed to save data! details: " + (xhr.responseText).split(".")[0]);
            $("#infoModal").modal();
        });
    }
});