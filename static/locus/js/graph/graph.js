function tweetTextNode(field, tweet) {
    switch (field) {
        case "username": {
            var a = document.createElement('a');
            var linkText = document.createTextNode(tweet.username);
            a.appendChild(linkText);
            a.href = tweet.userlink;
            a.target = "_blank";
            return a;
        }
        case "link": {
            var a = document.createElement('a');
            var linkText = document.createTextNode("link");
            a.appendChild(linkText);
            a.title = tweet.link;
            a.data_ogle = "tooltip";
            a.href = tweet.link;
            a.target = "_blank";
            return a;
        }
        default:
            return document.createTextNode(tweet[field]);
    }
}


function articleTextNode(field, article) {
    switch (field) {
        case "page": {
            var a = document.createElement('a');
            var linkText = document.createTextNode(article.page);
            a.appendChild(linkText);
            a.href = "http://"+article.page;
            a.target = "_blank";
            return a;
        }
        case "link": {
            var a = document.createElement('a');
            var linkText = document.createTextNode("link");
            a.appendChild(linkText);
            a.title = article.link;
            a.data_ogle = "tooltip";
            a.href = article.link;
            a.target = "_blank";
            return a;
        }
        default:
            return document.createTextNode((article[field] == null) ? "" : article[field]);
    }
}


function addTweetRow(tweet) {
    if (!document.getElementsByTagName) return;

    old_tbody = document.getElementById("tweetsTable").getElementsByTagName("tbody").item(0);
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

function addGoogleRow(google) {
    if (!document.getElementsByTagName) return;

    old_tbody = document.getElementById("googleTable").getElementsByTagName("tbody").item(0);
    row = document.createElement("tr");

    let fields = ["date", "page", "link"];

    for (let field of fields) {
        let cell = document.createElement("td");
        let textnode = articleTextNode(field, google);
        cell.appendChild(textnode);
        row.appendChild(cell);
    }

    old_tbody.appendChild(row);
}

function addArticleRow(article) {
    if (!document.getElementsByTagName) return;

    old_tbody = document.getElementById("databaseTable").getElementsByTagName("tbody").item(0);
    row = document.createElement("tr");

    let fields = ["date", "page", "link", "similarity", "title", "words"];

    for (let field of fields) {
        let cell = document.createElement("td");
        let textnode = articleTextNode(field, article);
        cell.appendChild(textnode);
        row.appendChild(cell);
    }

    old_tbody.appendChild(row);
}

function addNode(node) {
    switch(node.group){
        case 'tweet':
            addTweetRow(node.tweet);
            break;
        case 'google':
            addGoogleRow(node.google);
            break;
        case 'article':
            addArticleRow(node.article);
            break;
    }
}

var network;
var container;
var nodes;

function openTab(selectedNodes) {

    let lastItem = selectedNodes.slice(-1)[0];
    let lastNode = nodes.find(x => x.id === lastItem);

    if (lastNode !== undefined) {

        switch (lastNode.group) {
            case 'tweet':
                $('#pills-tab a[href="#pills-twitter"]').tab('show')
                break;
            case 'google':
                $('#pills-tab a[href="#pills-google"]').tab('show')
                break;
            case 'article':
                $('#pills-tab a[href="#pills-database"]').tab('show')
                break;
        }
    }

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
            hover: true,
        },
        edges: {
            color: {
                color: '#737373',
                highlight: '#404040',
            }
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
            google: {
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
    container = document.getElementById('mynetworkFA5');

    $.ajax({
        method: "GET",
        url: '/api/graph',
        success: function (graph) {

            nodes = graph.nodes;

            network = new vis.Network(container, graph, graphOptions);

            makeMeMultiSelect(container, network, nodes);

            network.on('click', function (properties) {
                clearTables();

                properties.nodes.forEach(function (item, index) {
                    node = nodes.find(x => x.id === item);
                    addNode(node)
                });

                openTab(properties.nodes)
            });

        },
        error: function (errorData) {
            console.error(errorData)
        }
    });
}

const tables = ["tweetsTable", "googleTable", "databaseTable"]

function clearTables() {
    tables.forEach(function (item, index) {
        let table = document.getElementById(item);
        let old_tbody = table.getElementsByTagName("tbody").item(0);
        old_tbody.parentNode.replaceChild(document.createElement('tbody'), old_tbody);
    });
}

function getPosition(el) {
  var xPos = 0;
  var yPos = 0;
 
  while (el) {
    if (el.tagName == "BODY") {
      // deal with browser quirks with body/window/document and page scroll
      var xScroll = el.scrollLeft || document.documentElement.scrollLeft;
      var yScroll = el.scrollTop || document.documentElement.scrollTop;
 
      xPos += (el.offsetLeft - xScroll + el.clientLeft);
      yPos += (el.offsetTop - yScroll + el.clientTop);
    } else {
      // for all other non-BODY elements
      xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
      yPos += (el.offsetTop - el.scrollTop + el.clientTop);
    }
 
    el = el.offsetParent;
  }
  return {
    x: xPos,
    y: yPos
  };
}

// Handle the right clic rectangle selection of nodes
// ========

const NO_CLICK = 0;
const RIGHT_CLICK = 3;

// Selector
function canvasify(DOMx, DOMy) {
    const { x, y } = network.DOMtoCanvas({ x: DOMx, y: DOMy });
    return [x, y];
}

function correctRange(start, end){
    return start < end ? [start, end] : [end, start];
}

function selectFromDOMRect(){
    const [sX, sY] = canvasify(DOMRect.startX, DOMRect.startY);
    const [eX, eY] = canvasify(DOMRect.endX, DOMRect.endY);
    const [startX, endX] = correctRange(sX, eX);
    const [startY, endY] = correctRange(sY, eY);

    network.selectNodes(nodes.reduce(
        (selected, { id }) => {
            const { x, y } = network.getPositions(id)[id];
            return (startX <= x && x <= endX && startY <= y && y <= endY) ? selected.concat(id) : selected;
            //And nodes.get(id).hidden ? Depending on the behavior expected
        }, []
    ));

    clearTables();

    network.getSelectedNodes().forEach(function (item, index) {
        node = nodes.find(x => x.id === item);
        addNode(node)
    });
}

function rectangle_mousedown(evt){
    // Handle mouse down event = beginning of the rectangle selection

    var pageX = event.pageX;    // Get the horizontal coordinate
    var pageY = event.pageY;    // Get the vertical coordinate
    var which = event.which;    // Get the button type

    offset = getPosition(container);

    // When mousedown, save the initial rectangle state
    if(which === RIGHT_CLICK) {
        Object.assign(DOMRect, {
            startX: pageX - offset.x,
            startY: pageY - offset.y,
            endX: pageX - offset.x,
            endY: pageY - offset.y
        });
        drag = true;
    }
}

function rectangle_mousedrag(evt){
    // Handle mouse drag event = during the rectangle selection
    var pageX = event.pageX;    // Get the horizontal coordinate
    var pageY = event.pageY;    // Get the vertical coordinate
    var which = event.which;    // Get the button type

    if(which === NO_CLICK && drag) {
        // Make selection rectangle disappear when accidently mouseupped outside 'container'
        drag = false;
        network.redraw();
    } else if(drag) {
        // When mousemove, update the rectangle state

        offset = getPosition(container);

        Object.assign(DOMRect, {
            endX: pageX - offset.x,
            endY: pageY - offset.y
        });
        network.redraw();
    }
}

function rectangle_mouseup(evt){
    // Handle mouse up event = beginning of the rectangle selection

    var pageX = event.pageX;    // Get the horizontal coordinate
    var pageY = event.pageY;    // Get the vertical coordinate
    var which = event.which;    // Get the button type

    // When mouseup, select the nodes in the rectangle
    if(which === RIGHT_CLICK) {
        drag = false;
        network.redraw();
        selectFromDOMRect();
    }


}

function draw_rectangle_on_network(ctx){
    // Draw a rectangle regarding the current selection
    if(drag) {
        const [startX, startY] = canvasify(DOMRect.startX, DOMRect.startY);
        const [endX, endY] = canvasify(DOMRect.endX, DOMRect.endY);

        ctx.setLineDash([5]);
        ctx.strokeStyle = 'rgba(78, 146, 237, 0.75)';
        ctx.strokeRect(startX, startY, endX - startX, endY - startY);
        ctx.setLineDash([]);
        ctx.fillStyle = 'rgba(151, 194, 252, 0.45)';
        ctx.fillRect(startX, startY, endX - startX, endY - startY);
    }
}


function makeMeMultiSelect(container, network, nodes) {
    // State
    drag = false;
    DOMRect = {};

    // Disable default right-click dropdown menu
    container.oncontextmenu = () => {$(window).scrollTop(0); return false;};

    // Listeners
    //container.mousedown()
    $(document).on("mousedown", function(evt) { rectangle_mousedown(evt) });
    $(document).on("mousemove", function(evt) { rectangle_mousedrag(evt) });
    $(document).on("mouseup", function(evt) { rectangle_mouseup(evt) });

    // Drawer
    network.on('afterDrawing', function (ctx) { draw_rectangle_on_network(ctx) });
}