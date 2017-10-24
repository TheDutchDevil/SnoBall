

function sendQueryToMain() {
    var url = window.location.origin;

    var query = $("#query-header").val();

    window.location.assign(url + "/?q=" + encodeURI(query));

    return false;
}

window.onload = function() {
    $("#query-header").keyup(function (event) {
        if (event.keyCode === 13) {
            $("#id_of_button").click();
        }
    });
};
