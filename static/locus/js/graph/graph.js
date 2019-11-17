function tweetTextNode(field, tweet) {
    switch (field) {
        case "username": {
            var a = document.createElement('a');
            var linkText = document.createTextNode(tweet.username);
            a.appendChild(linkText);
            a.title = tweet.username;
            a.href = tweet.userlink;
            a.target = "_blank";
            return a;
        }
        case "link": {
            var a = document.createElement('a');
            var linkText = document.createTextNode(tweet.link);
            a.appendChild(linkText);
            a.title = "link";
            a.href = tweet.link;
            a.target = "_blank";
            return a;
        }
        default:
            return document.createTextNode(tweet[field]);
    }
}


function addRow(tweet) {
    if (!document.getElementsByTagName) return;

    old_tbody = document.getElementsByTagName("tbody").item(0);

    row = document.createElement("tr");

    let fields = ["date", "time", "username", "content", "likes", "replies", "retweets", "link"];

    for (let field of fields) {
        let cell = document.createElement("td");
        let textnode = tweetTextNode(field, tweet);
        cell.appendChild(textnode);
        row.appendChild(cell);
    }

    old_tbody.appendChild(row);

}


function draw() {

    var graphOptions = {
        layout: {
            randomSeed: 8
        },
        physics: {
            adaptiveTimestep: false
        },
        interaction: {
            navigationButtons: true,
            keyboard: true,
            multiselect: true,
        },
        groups: {
            article: {
                shape: 'icon',
                icon: {
                    face: "'Font Awesome 5 Free'",
                    weight: "bold", // Font Awesome 5 doesn't work properly unless bold.
                    code: '\uf15c',
                    size: 40,
                    color: '#333399'
                }
            },
            page: {
                shape: 'icon',
                icon: {
                    face: "'Font Awesome 5 Free'",
                    weight: "bold", // Font Awesome 5 doesn't work properly unless bold.
                    code: '\uf7a2',//'\uf0ac',
                    size: 40,
                    color: '#009933'
                }
            },
            user: {
                shape: 'icon',
                icon: {
                    face: "'Font Awesome 5 Free'",
                    weight: "bold", // Font Awesome 5 doesn't work properly unless bold.
                    code: '\uf007',
                    size: 40,
                    color: '#57169a'
                }
            },
            search: {
                shape: 'icon',
                icon: {
                    face: "'Font Awesome 5 Free'",
                    weight: "bold", // Font Awesome 5 doesn't work properly unless bold.
                    code: '\uf002',
                    size: 50,
                    color: '#e68a00'
                }
            },
            tweet: {
                shape: 'icon',
                icon: {
                    face: "'Font Awesome 5 Brands'",
                    weight: "bold", // Font Awesome 5 doesn't work properly unless bold.
                    code: '\uf099',
                    size: 30,
                    color: '#0084b4'
                }
            }
        }
    };

    // create a network
    var containerFA5 = document.getElementById('mynetworkFA5');

    $.ajax({
        method: "GET",
        url: '/api/graph',
        success: function (graph) {

            nodes = graph.nodes;

            var network = new vis.Network(containerFA5, graph, graphOptions);


            network.on('click', function (properties) {


                item = document.getElementsByTagName("tbody").item(0);
                item.parentNode.replaceChild(document.createElement('tbody'), item);

                /*
                document.getElementsByTagName("tbody").forach(function(item, index){
                  item.parentNode.replaceChild(document.createElement('tbody'), item);
                });
                */


                properties.nodes.forEach(function (item, index) {
                    node = nodes.find(x => x.id === item);
                    addRow(node.tweet)
                });


            });

        },
        error: function (errorData) {
            console.error(errorData)
        }
    });
}