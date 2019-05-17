// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const tweetsEndpoint = '/api/tweets';
const yearlyTweetsEndpoint = tweetsEndpoint + '/yearly';
const monthlyTweetsEndpoint = tweetsEndpoint + '/monthly';
const dailyTweetsEndpoint = tweetsEndpoint + '/daily';

let dailyActiveChart;
let monthlyActiveChart;

let defaultChartConfig = {
    type: 'bar',
    data: {
      datasets: [{
        label: "Tweets",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
      }],
    },
    options: {
      scales: {
        xAxes: [{
          time: {
          },
          gridLines: {
            display: false
          },
          /*
          ticks: {
            maxTicksLimit: 12
          }
          */
          maxBarThickness: 20,
        }],
        yAxes: [{
          ticks: {
            min: 0,
            suggestedMax: 5,
            precision: 0
          },
          gridLines: {
            display: true
          }
        }],
      },
      legend: {
        display: false
      },
    }
  };

function initYearlyActiveChart(year){
  $.ajax({
    method: "GET",
    url: yearlyTweetsEndpoint,
    success: function (data) {
      setYearlyActiveChart(data.activity, data.minYear, data.maxYear);
      initMonthlyActiveChart(data.minYear)
    },
    error: function (errorData) {
      console.error(errorData)
    }
});
}

function initMonthlyActiveChart(year){
  $.ajax({
    method: "GET",
    url: monthlyTweetsEndpoint,
    data: {
      "year": year,
    },
    success: function (data) {
        var ele= document.getElementsByClassName("year")
        for(var i=0;i<ele.length;i++)
        {
          ele[i].innerHTML=year;
        }
      setMonthlyActiveChart(data);
      initDailyActiveChart(1)
    },
    error: function (errorData) {
      console.error(errorData)
    }
  });
}

function initDailyActiveChart(month){
  $.ajax({
    method: "GET",
    url: dailyTweetsEndpoint,
    data: {
      "month": month,
    },
    success: function (data) {
      document.getElementById("month").innerHTML = months[month-1];
      setDailyActiveChart(data);
    },
    error: function (errorData) {
      console.error(errorData)
    }
});
}

function setYearlyActiveChart(chartData, minYear, maxYear) {
  let ctx = document.getElementById("yearlyActiveChart");

  let chartConfig = JSON.parse(JSON.stringify(defaultChartConfig));
  chartConfig.data.labels = Array.from({length: maxYear - minYear + 1}, (v, k) => k+minYear);
  chartConfig.data.datasets[0].data = chartData;
  chartConfig.options.scales.xAxes[0].time.unit = 'year';
  chartConfig.options.onClick = function(c,i) {
          let e = i[0];
          let x_value = this.data.labels[e._index];
          let y_value = this.data.datasets[0].data[e._index];
          initMonthlyActiveChart(x_value)
      };
  let yearlyActiveChart = new Chart(ctx, chartConfig);
}

function setMonthlyActiveChart(chartData) {
  let ctx = document.getElementById("monthlyActiveChart");
  if (monthlyActiveChart !== undefined) {
    monthlyActiveChart.destroy();
  }

  let chartConfig = JSON.parse(JSON.stringify(defaultChartConfig));
  chartConfig.data.labels = months.map(function(month) {
        return month.substr(0,3);
      });
  chartConfig.data.datasets[0].data = chartData;
  chartConfig.options.scales.xAxes[0].time.unit = 'month';
  chartConfig.options.onClick = function(c,i) {
          let e = i[0];
          let x_value = this.data.labels[e._index];
          let y_value = this.data.datasets[0].data[e._index];
          initDailyActiveChart(e._index + 1)
      };
  monthlyActiveChart = new Chart(ctx, chartConfig);
}

function setDailyActiveChart(chartData){
  let ctx = document.getElementById("dailyActiveChart");
  if (dailyActiveChart !== undefined) {
    dailyActiveChart.destroy();
  }

  let chartConfig = JSON.parse(JSON.stringify(defaultChartConfig));
  chartConfig.data.labels = Array.from({length: 31}, (v, k) => k+1);
  chartConfig.data.datasets[0].data = chartData;
  chartConfig.options.scales.xAxes[0].time.unit = 'day';
  chartConfig.options.onClick = function(c,i) {};

  dailyActiveChart = new Chart(ctx, chartConfig);
}

initYearlyActiveChart();