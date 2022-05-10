$(document).ready(function() {
    console.log("script successfully started");
    var url = "/site/categories.json";

    var json = $.getJSON(url, function(data) {
        console.log("Data has been successfully received:");
        console.log(data["categories"]);

        for(var i = 0; i < 6; i++) {
            var entry = data["categories"][i];

            var j = i + 1;
            var category_id = "#category" + j;
            var table_id = "#" + entry.table;

            $(category_id).text(entry.cName);
            $(table_id + "_a").text(entry.price);
            $(table_id + "_b").text(entry.viewsD);
            $(table_id + "_c").text(entry.viewsT);
            $(table_id + "_d").text(entry.ads);
        }
    });

    $("#submit").click(function() {
        var user_data = [];

        user_data[0] = String($("#age").val());
        user_data[1] = String($("#ed").val());
        user_data[2] = String($("#ms").val());
        user_data[3] = String($("#occ").val());
        user_data[4] = String($("#hrs").val());

        console.log(user_data);
    });
})
