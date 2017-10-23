var resultsTemplate;

authorTotal = 8356;

function sendQuery() {
    var query_string = $("#query_input").val();

    $.ajax({
        url: '/sendquery',
        type: 'POST',
        data: query_string,
        success: function (response) {
            var result = JSON.parse(response);

            var items = [];
            for (var i = 0; i < Math.min(result['items'].length, 20); i++) {

                var item = result.items[i];

                if (item.type === "paper") {
                    item.isPaper = true;
                } else if (item.type === "author") {

                    if (item.rank <= authorTotal / 100) {
                        item.isDiamond = true;
                    } else if (item.rank <= (authorTotal / 100) * 5) {
                        item.isGold = true;
                    } else if (item.rank <= (authorTotal / 100) * 10) {
                        item.isSilver = true;
                    } else if (item.rank <= (authorTotal / 100) * 25) {
                        item.isBronze = true;
                    } else {
                        item.noBadge = true;
                    }


                    item.isAuthor = true;
                } else if (item.type === "topic") {
                    item.isTopic = true;
                }


                items.push(result.items[i]);
            }

            var html = resultsTemplate(items);

            $('#result_paper').html(html);
        }
    });
}

window.onload = function () {
    var source = $("#results-template").html();
    resultsTemplate = Handlebars.compile(source);

    Handlebars.registerHelper('eq', function (val, val2, block) {
        if (val == val2) {
            return block(this);
        }
    });
};

Handlebars.registerHelper('compare', function (lvalue, rvalue, options) {

    if (arguments.length < 3)
        throw new Error("Handlerbars Helper 'compare' needs 2 parameters");

    var operator = options.hash.operator || "==";

    var operators = {
        '==': function (l, r) {
            return l == r;
        },
        '===': function (l, r) {
            return l === r;
        },
        '!=': function (l, r) {
            return l != r;
        },
        '<': function (l, r) {
            return l < r;
        },
        '>': function (l, r) {
            return l > r;
        },
        '<=': function (l, r) {
            return l <= r;
        },
        '>=': function (l, r) {
            return l >= r;
        },
        'typeof': function (l, r) {
            return typeof l == r;
        }
    }

    if (!operators[operator])
        throw new Error("Handlerbars Helper 'compare' doesn't know the operator " + operator);

    var result = operators[operator](lvalue, rvalue);

    if (result) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }

});