$(document).ready(function() {
    console.log("script successfully started");
    var url = "/api/data";

    const button = $("#submit");

    button.click((e) => {

        button.prop("disabled", true);
        
        var request = {
            age : $("#age").val(),
            education : $("#ed").val(),
            maritalStatus : $("#ms").val(),
            occupation : $("#occ").val(),
            hours : $("#hrs").val()
        }

        $.ajax(url, {
            type: "GET",
            data: request,
            success: (data) => {
                console.log(data);
                $("#pred").text(data.result ? "Expected over 50k/ year" : "Expected under 50k/ year");
                button.text("Try again");
                button.prop("disabled", false);

            }
        });
        
    });
})
