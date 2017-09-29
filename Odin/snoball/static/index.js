function sendQuery()
{
    var query_string = $("#query_input").val();

    $.ajax({
        url: '/sendquery',
        type: 'POST',
        data: query_string,
        success: function(response){
            var result = JSON.parse(response);

            var html_string_papers = "<ul>";
            for(var i = 0; i < result['papers'].length; i++){
                html_string_papers += "<li><p>" + result['papers'][i].title + "</p></li>";
            }
            $("#result_paper").html(html_string_papers + "</ul>");
        }
    });
}