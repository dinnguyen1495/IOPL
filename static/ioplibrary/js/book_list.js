function update_book_list(data) {
    let filtered_list = "";
    for (let i = 0; i < data["books"].length; i++) {
        filtered_list +=
            "<div class=\"book-container\">\n" +
            "    <img class=\"book-cover\" src=\"" + data["books"][i]["cover"] + "\" alt=\"\"/>\n" +
            "    <div class=\"book-information\">\n" +
            "        <ul class=\"book-information-list\">\n" +
            "            <li><b>Title:</b> " + data["books"][i]["title"] + "</li>\n" +
            "            <li><b>Authors:</b> " + data["books"][i]["authors"] + "</li>\n" +
            "            <li><b>Publisher:</b> " + data["books"][i]["publisher"] + "</li>\n" +
            "            <li><b>Book:</b> " + data["books"][i]["type"] + "</li>\n" +
            "            <li><b>Field:</b> " + data["books"][i]["field"] + "</li>\n" +
            "            <li><b>Year:</b> " + data["books"][i]["year"] + "</li>\n" +
            "            <li><b>Edition:</b> " + data["books"][i]["edition"] + "</li>\n" +
            "            <li><b>ISBN:</b> " + data["books"][i]["isbn"] + "</li>\n" +
            "            <li><b>Inventory Number:</b> " + data["books"][i]["inventory_number"] + "</li>\n" +
            "            <li><b>Available:</b> " + data["books"][i]["available"] + "</li>\n" +
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
    let type = $('input[name=book_type]:radio:checked').val();
    let field = $('input[name=field]:radio:checked').val();
    let column = $('input[name=column]:radio:checked').val().toLowerCase();

    $.ajax({
        url: '/search/',
        type: "get",
        data: {
            'query': query,
            'book_type': type,
            'field': field,
            'column': column
        },
        success: function(data) {
            update_book_list(data);
        },
        dataType: "json"
    });
}

$('#search-form').submit(function(e) {
    e.preventDefault();
    return false;
});

$('#search-bar').on('input',function(e) {
    search_book();
});

$('input[name=book_type]').on('input',function(e) {
    search_book();
    $('#search-bar').focus();
});

$('input[name=field]').on('input',function(e) {
    search_book();
    $('#search-bar').focus();
});

$('input[name=column]').on('input',function(e) {
    search_book();
    $('#search-bar').focus();
});