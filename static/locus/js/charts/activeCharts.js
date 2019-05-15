// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const tweetsEndpoint = '/api/tweets';
const monthlyTweetsEndpoint = tweetsEndpoint + '/monthly';
const dailyTweetsEndpoint = tweetsEndpoint + '/daily';

let dailyActiveChart;

$.ajax({
    method: "GET",
    url: monthlyTweetsEndpoint,
    success: function (data) {
      setMonthlyActiveChart(data)
    },
    error: function (errorData) {
      console.error(errorData)
    }
});

function setMonthlyActiveChart(chartData) {
  let ctx = document.getElementById("monthlyActiveChart");
  let myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: months.map(function(month) {
        return month.substr(0,3);
      }),
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
          let e = i[0];
          let x_value = this.data.labels[e._index];
          let y_value = this.data.datasets[0].data[e._index];

          $.ajax({
            method: "GET",
            url: dailyTweetsEndpoint,
            data: {
              "month": e._index + 1,
            },
            success: function (data) {
              document.getElementById("month").innerHTML = months[e._index];
              setDailyActiveChart(data);
            },
            error: function (errorData) {
              console.error(errorData)
            }
        });
      }
    }
  });
}

function setDailyActiveChart(chartData){
  let ctx = document.getElementById("dailyActiveChart");
  if (dailyActiveChart !== undefined) {
    dailyActiveChart.destroy();
  }
  dailyActiveChart = new Chart(ctx, {
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
}