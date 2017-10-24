var resultsTemplate;

authorTotal = 8356;
paperTotal = 6560;

function addMedalsToAuthor(author) {
    if (author.rank <= authorTotal / 100) {
        author.isDiamond = true;
    } else if (author.rank <= (authorTotal / 100) * 5) {
        author.isGold = true;
    } else if (author.rank <= (authorTotal / 100) * 10) {
        author.isSilver = true;
    } else if (author.rank <= (authorTotal / 100) * 25) {
        author.isBronze = true;
    } else {
        author.noBadge = true;
    }
}

function addMedalsToPaper(paper) {
    if (paper.rank <= paperTotal / 100) {
        paper.isDiamond = true;
    } else if (paper.rank <= (paperTotal / 100) * 5) {
        paper.isGold = true;
    } else if (paper.rank <= (paperTotal / 100) * 10) {
        paper.isSilver = true;
    } else if (paper.rank <= (paperTotal / 100) * 25) {
        paper.isBronze = true;
    } else {
        paper.noBadge = true;
    }
}

function sendQueryUrl(query_string) {
    var searchParams = new URLSearchParams(window.location.search)
    searchParams.set("q", query_string);
    var newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
    history.pushState(null, '', newRelativePathQuery);

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
                    item.authors.forEach(function (author) {
                        addMedalsToAuthor(author)
                    });

                    addMedalsToPaper(item);

                    item.isPaper = true;
                } else if (item.type === "author") {
                    addMedalsToAuthor(item);
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


function sendQuery() {
    var queryString = $("#query_input").val();

    sendQueryUrl(queryString);
}

function readQueryStrings() {
    var searchParams = new URLSearchParams(window.location.search);

    var query = searchParams.get("q");

    if (query !== null) {
        $("#query_input").val(query);
        sendQueryUrl(query);
    }
}

readQueryStrings();

window.onload = function () {
    var source = $("#results-template").html();
    resultsTemplate = Handlebars.compile(source);

    Handlebars.registerHelper('eq', function (val, val2, block) {
        if (val == val2) {
            return block(this);
        }
    });

        $("#query_input").keyup(function (event) {
        if (event.keyCode === 13) {
            $("#main-query-button").click();
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