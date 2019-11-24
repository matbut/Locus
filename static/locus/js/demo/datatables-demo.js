// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});


const crawlers = ["tweet_crawler", "google_crawler", "db_searcher"];

const crawlerEndpoint = '/api/crawler';

var active = {
  "tweet_crawler": false,
  "google_crawler": false,
  "db_searcher": false
};

document.getElementById("tweetCrawlerDropdown").addEventListener('click', function(){
  poolWhileActive("tweet_crawler")
});
document.getElementById("googleCrawlerDropdown").addEventListener('click', function(){
  poolWhileActive("google_crawler")
});
document.getElementById("databaseSearcher").addEventListener('click', function(){
  poolWhileActive("db_searcher")
});


function poolWhileActive(crawler) {
  if(!active[crawler]) {
    active[crawler] = true;
    fillCrawler(crawler);
  } else {
    active[crawler] = false;
  }
}


function fillCrawler(crawler){
  $.ajax({
    method: "GET",
    url: crawlerEndpoint,
    data: {
      "crawler": crawler,
    },
    success: function (data) {
      crawlerElement = document.getElementById(crawler);
      crawlerElement.querySelector('.working').innerHTML = data.working;
      crawlerElement.querySelector('.completed').innerHTML = data.completed;
      crawlerElement.querySelector('.failed').innerHTML = data.failed;
    },
    error: function (errorData) {
      console.error(errorData)
    }
  });
  if(active[crawler]) {
    setTimeout(function() {
      fillCrawler(crawler);
    }, 1000);
  }
}