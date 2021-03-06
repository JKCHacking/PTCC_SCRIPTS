$(document).ready(function(e) {
    $("#generate_lr").on("click", function() {
        var html_string;
        var employee_name;

        $("#infoModal").modal();
        $(".info-modal-title").html("Generate All Employees");
        html_string = "<h6>These are the employees that will generate Leave Registry: </h6>";
        $.each($('input.form-check-input'), function() {
            if ($(this).prop("checked")) {
                employee_name = $(this).data("empname");
                html_string += "<h6>* <strong>"+ employee_name + "</strong></h6>"
                checked_employee_list.push($(this).data("id"));
            }
        });

        if (checked_employee_list.length == 0) {
            html_string = "<h6>No selected employees.</h6>"
            $("#generate_button").attr("disabled", true);
        } else {
            $("#generate_button").attr("disabled", false);
        }

        $(".info-modal-body").html(html_string);
        $("#generate_button").attr("hidden", false);
        $("#year_selection").attr("hidden", false);
        populateYearSelection();
    });

    $("#check_all_employee").click(function() {
        if($(this).prop("checked")) {
            $("input.form-check-input").prop("checked", true);
        } else {
            $("input.form-check-input").prop("checked", false);
        }
    });

    $("#generate_button").on("click", function(){
        $("#generate_button").attr("hidden", true);
        $("#year_selection").attr("hidden", true);
        requestGenerate();
    });

    $(document).on("click", ".sidebar_button", function() {
        $("#uploadModal").modal();
        id = $(this).attr("id");
        $("#upload_label").html("<h6>Please upload CSV File in either of the following:</h6>" +
                                 "<h6>1. employee.csv</h6>" +
                                 "<h6>2. leaves.csv</h6>" +
                                 "<h6>3. offenses.csv</h6>" +
                                 "<h6>4. earned_leaves.csv</h6>"+
                                 "<h6>5. timesheet.csv</h6>");

        $("#uploadModalLabel").html("Upload CSV File");
    });

    $("#info_button_close").on("click", function() {
        $("#generate_button").attr("hidden", true);
        $("#year_selection").attr("hidden", true);
        location.reload();
    });

    $("#upload_form").submit(function(e) {
        e.preventDefault();
        var formData = new FormData($(this)[0]);
        $.ajax({
            url:url_upload,
            type: "POST",
            data: formData,
            async: false,
            cache: false,
            contentType: false,
            enctype: "multipart/form-data",
            processData: false,
        })
        .done(function(response) {
            $(".info-modal-title").html(response.head);
            $(".info-modal-body").html(response.body);
            $("#infoModal").modal();
            $("#uploadModal").modal('hide');
        })
        .fail(function(xhr, status, error){
            $(".info-modal-title").html("Failed");
            $(".info-modal-body").html("Failed to save data! details: " + (xhr.responseText).split(".")[0]);
            $("#infoModal").modal();
        });
    });

    $("body").on("click", '#download_button', function(e) {
        var filename = $(this).data("file");
        var request = new XMLHttpRequest();
        var data = "filename="+filename;
        request.open('POST', url_download, true);
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.responseType = 'blob';

        request.onload = function(e) {
            if (this.status == 200) {
                var blob = this.response
                if (window.navigator.msSaveOrOpenBlob) {
                    window.navigator.msSaveBlob(blob, filename);
                } else {
                    var downloadLink = window.document.createElement('a');
                    var contentTypeHeader = request.getResponseHeader("Content-Type");
                    downloadLink.href = window.URL.createObjectURL(new Blob([blob], {type: contentTypeHeader}));
                    downloadLink.download = filename;
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                }
            } else {
                alert('Download Failed');
            }
        };
        request.send(data);
    });

    function populateYearSelection() {
        var start_year = 2000;
        var end_year = new Date().getFullYear();
        var options = "";
        for (var year = end_year; year >= start_year; year-- ) {
            options += "<option value=" + year +">"+ year + "</option>";
        }
        $("#year_selection").html(options);
    }

    function requestGenerate() {
        console.log(checked_employee_list);
        var selected_year = $("#year_selection option:selected").text();
        var data = {
            "checked_employees":checked_employee_list,
            "year": selected_year
        };
        $.ajax({
            url:url_generate,
            type:"POST",
            data:data
        })
        .done(function(response){
            var file_name = response.data;
            dl_button_html = "<button type='button' class='btn btn-primary' data-file=" + file_name + " id='download_button'>Download File</button>";
            $(".info-modal-title").html(response.head);
            $(".info-modal-body").html(response.body);
            $(".modal-footer").append(dl_button_html);
            $("#infoModal").modal();
            checked_employee_list = [];
        })
        .fail(function(xhr, status, error) {
            $(".info-modal-title").html("Failed");
            $(".info-modal-body").html("Failed to save data! details: " + (xhr.responseText).split(".")[0]);
            $("#infoModal").modal();
        });
    }
});