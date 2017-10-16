
var resultsTemplate;

function sendQuery()
{
    var query_string = $("#query_input").val();

    $.ajax({
        url: '/sendquery',
        type: 'POST',
        data: query_string,
        success: function(response){
            var result = JSON.parse(response);

            var items = [];
            for(var i = 0; i < Math.min(result['items'].length, 20); i++){

                var item = result.items[i];

                if(item.type === "paper") {
                    item.isPaper = true;
                } else if (item.type === "author") {
                    item.isAuthor = true;
                }


                items.push(result.items[i]);
            }

            var html = resultsTemplate(items);

            $('#result_paper').html(html);
        }
    });
}

window.onload = function () {
    var source   = $("#results-template").html();
    resultsTemplate = Handlebars.compile(source);

    Handlebars.registerHelper('eq', function(val, val2, block) {
      if(val == val2){
        return block(this);
      }
    });
}