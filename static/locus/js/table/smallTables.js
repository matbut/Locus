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

function openTab(selectedNodes) {
      switch (selectedNodes) {
          case 'tweets':
              $('#pills-tab a[href="#pills-twitter"]').tab('show')
              break;
          case 'google':
              $('#pills-tab a[href="#pills-google"]').tab('show')
              break;
          case 'database':
              $('#pills-tab a[href="#pills-database"]').tab('show')
              break;
      }
}

const tables = ["tweetsTable", "googleTable", "databaseTable"];

function clearTables() {
    tables.forEach(function (item, index) {
        let table = document.getElementById(item);
        let old_tbody = table.getElementsByTagName("tbody").item(0);
        old_tbody.parentNode.replaceChild(document.createElement('tbody'), old_tbody);
    });
}