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
            for(var i = 0; i < result['items'].length; i++){
                var temp = result['items'][i];
                var html_string_authors = "";
                for(var j = 0; j < temp.authors.length; j++){
                    var pre = ", ";
                    if(j == 0){
                        pre = "";
                    }
                    html_string_authors += (pre + "<a href='#' id='author_link'>" + temp.authors[j] + "</a>");
                }
                html_string_papers += "<li><a href='/paper/details?id=1000'><p>" + temp.title + "</p></a>" + html_string_authors + "</li>";
            }
            $("#result_paper").html(html_string_papers + "</ul>");
        }
    });
}