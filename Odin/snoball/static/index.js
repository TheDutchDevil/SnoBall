function sendQuery()
{
    var query_string = $("#query_input").val();

    $.ajax({
        url: '/sendquery',
        type: 'POST',
        data: query_string,
        success: function(response){
            console.log(response);
        }
    });
}