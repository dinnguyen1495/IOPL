function update_book_list(data) {
    console.log(data);
    let filtered_list = "";
    for (let i = 0; i < data["books"].length; i++) {
        filtered_list +=
            "<div class=\"book-container\">\n" +
            "    <img class=\"book-cover\" src=\"" + data["books"][i]["cover"] + "\" alt=\"\"/>\n" +
            "    <div class=\"book-information\">\n" +
            "        <ul class=\"book-information-list\">\n" +
            "            <li>Title: " + data["books"][i]["title"] + "</li>\n" +
            "            <li>Authors: " + data["books"][i]["authors"] + "</li>\n" +
            "            <li>Publisher: " + data["books"][i]["publisher"] + "</li>\n" +
            "            <li>Field: " + data["books"][i]["field"] + "</li>\n" +
            "            <li>Year: " + data["books"][i]["year"] + "</li>\n" +
            "            <li>Edition: " + data["books"][i]["edition"] + "</li>\n" +
            "            <li>Available: " + data["books"][i]["available"] + "</li>\n" +
            "        </ul>\n" +
            "    </div>\n" +
            "</div>";
    }
    $("#book-list").html(
        filtered_list
    );
}

function search_book() {
    let query = $('#search-bar').val();
    let field = $('input[name=field]:radio:checked').val();
    let column = $('input[name=column]:radio:checked').val().toLowerCase();

    $.ajax({
        url: '/search/',
        type: "get",
        data: {
            'query': query,
            'field': field,
            'column': column
        },
        success: function (data) {
            update_book_list(data);
        },
        dataType: "json"
    });
}