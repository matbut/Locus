// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});


const crawlers = ["tweet_crawler", "google_crawler", "db_searcher"];

const crawlerEndpoint = '/api/crawler';

document.getElementById("tweetCrawlerDropdown").addEventListener('click', function(){
    fillCrawler("tweet_crawler");
});
document.getElementById("googleCrawlerDropdown").addEventListener('click', function(){
    fillCrawler("google_crawler");
});
document.getElementById("databaseSearcher").addEventListener('click', function(){
    fillCrawler("db_searcher");
});


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
}