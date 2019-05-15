// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var endpoint = '/api/chart/tweets/monthly';
var chartData = [];
$.ajax({
    method: "GET",
    url: endpoint,
    success: function (data) {
      chartData = data;
      setBarChart(data)
    },
    error: function (errorData) {
      console.error(errorData)
    }
});

function setBarChart(chartData) {
  var ctx = document.getElementById("monthlyActiveChart");
  var myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [{
        label: "Tweets",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: chartData,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'month'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 12
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            //max: 40000,
            //maxTicksLimit: 5
          },
          gridLines: {
            display: true
          }
        }],
      },
      legend: {
        display: false
      },
      events: ['click'],
      onClick: function(c,i) {
          e = i[0];
          console.log(e._index)
          var x_value = this.data.labels[e._index];
          var y_value = this.data.datasets[0].data[e._index];
          console.log(x_value);
          console.log(y_value);


          $.ajax({
            method: "GET",
            url: '/api/chart/tweets/daily',
            data: {
              "month": e._index + 1,
            },
            success: function (data) {
              updateLineChart(data);
            },
            error: function (errorData) {
              console.error(errorData)
            }
        });
      }
    }
  });
}
setLineChart(chartData);

var myLineChart;

function updateLineChart(data) {
  myLineChart.destroy();
  setLineChart(data);
}

function setLineChart(chartData){
  var ctx = document.getElementById("dailyActiveChart");
  myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Array.from({length: 31}, (v, k) => k+1),
      datasets: [{
        label: "Tweets",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: chartData,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
            unit: 'day'
          },
          gridLines: {
            display: false
          },
          ticks: {
            maxTicksLimit: 31
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            //max: 40000,
            //maxTicksLimit: 5
          },
          gridLines: {
            display: true
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });

  /*
  var ctx = document.getElementById("dailyActiveChart");
  var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: Array.from({length: 31}, (v, k) => k+1),
    datasets: [{
      label: "Tweets",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: chartData,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 31
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          //max: 40000,
          //maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
*/
}