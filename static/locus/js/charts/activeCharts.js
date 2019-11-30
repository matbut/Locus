var aggregation = 'week'

var options = {
  chart: {
    type: 'line',
    stacked: false,
    height: 500,
    zoom: {
      type: 'x',
      enabled: true,
      autoScaleYaxis: false
    },
    toolbar: {
      autoSelected: 'zoom',
      tools: {
        download: false,
        selection: true,
        zoom: '<i class="fas fa-cut"></i>',
        zoomin: '<i class="fas fa-search-plus"></i>',
        zoomout: '<i class="fas fa-search-minus"></i>',
        pan: true,
        reset: '<i class="fas fa-crosshairs"></i>',
        customIcons: []
      },
    },
    events: {
      zoomed: function (chartContext, {xaxis, yaxis}) {
        console.log('zoomed',xaxis.min, xaxis.max);
      },
      dataPointSelection: function(event, chartContext, config) {
        console.log('dataPointSelection', event);
      }
    },
  },
  colors:['#0084b4', '#00b435', '#7b3db4'],
  dataLabels: {
    enabled: false
  },
  series: [],
  markers: {
    size: 5,
  },
  title: {
    text: 'Activity',
    align: 'left'
  },
/*  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      inverseColors: false,
      opacityFrom: 0.5,
      opacityTo: 0,
      stops: [0, 90, 100]
    },
  },*/
  yaxis: {
    labels: {
    },
    title: {
      text: 'Activity'
    },
  },
  xaxis: {
    type: 'datetime',
    title: {
      //text: 'Time'
    },
  },
  tooltip: {
    shared: false, //true looks good
    intersect: true,
    x: {
      format: "d MMM yyyy"
    },
  }
};

var chart = new ApexCharts(
  document.querySelector("#chart"),
  options
);
chart.render();

updateDataBy(aggregation);

function updateDataBy(aggregate) {
  $.ajax({
    method: "GET",
    url: '/api/chart',
    data: {
      aggregate: aggregate,
    },
    success: function (data) {
      chart.updateSeries(data, true)
    },
    error: function (errorData) {
      console.error(errorData)
    }
  });
}

showTweetButton = document.getElementById("show_tweet_results");
showGoogleButton = document.getElementById("show_google_results");
showDatabaseButton = document.getElementById("show_database_results");

showButtons = [showTweetButton, showGoogleButton, showDatabaseButton];

showTweetButton.addEventListener("click", function(){toggleSeries(showTweetButton, "Tweets")});
showGoogleButton.addEventListener("click", function(){toggleSeries(showGoogleButton, "Google")});
showDatabaseButton.addEventListener("click", function(){toggleSeries(showDatabaseButton, "Database")});

function toggleSeries(checkBox, series) {
  if (checkBox.classList.contains('btn-outline-primary'))
    checkBox.classList.replace('btn-outline-primary', 'btn-primary');
  else
    checkBox.classList.replace('btn-primary', 'btn-outline-primary');

  chart.toggleSeries(series)
}

reloadButton = document.getElementById("reloadButton")

dayAggregateButton = document.getElementById('dayAggregate');
weekAggregateButton = document.getElementById('weekAggregate');
monthAggregateButton = document.getElementById('monthAggregate');
yearAggregateButton = document.getElementById('yearAggregate');

aggregateButtons = [dayAggregateButton, monthAggregateButton, weekAggregateButton, yearAggregateButton];

function changeActiveTo(clickedButton) {
  for (let button of aggregateButtons) {
    button.classList.remove("active")
  }
  clickedButton.classList.add("active");

  for (let button of showButtons) {
    button.classList.replace('btn-outline-primary', 'btn-primary');
  }

  switch (clickedButton) {
    case dayAggregateButton:
      aggregation = 'day';
      chart.updateOptions({
        chart: {
          type: 'line',
        },
        xaxis: {
          labels: {
            datetimeFormatter: {
              year: 'yyyy',
              month: 'MMM \'yy',
              day: 'dd MMM',
              hour: 'HH:mm'
            }
          }
        },
        tooltip: {
          x: {
            format: "d MMM yyyy"
          }
        }
      });
      break;
    case weekAggregateButton:
      aggregation = 'week';
      chart.updateOptions({
        chart: {
          type: 'line',
        },
        xaxis: {
          labels: {
            datetimeFormatter: {
              year: 'yyyy',
              month: 'MMM \'yy',
              day: 'dd MMM',
              hour: 'HH:mm'
            }
          }
        },
        tooltip: {
          x: {
            format: "d MMM yyyy"
          }
        }
      });
      break;
    case monthAggregateButton:
      aggregation = 'month';
      chart.updateOptions({
        chart: {
          type: 'bar',
        },
        xaxis: {
          labels: {
            format: 'MMM yyyy',
          }
        },
        tooltip: {
          x: {
            format: "MMM yyyy"
          }
        }
      });
      break;
    case yearAggregateButton:
      aggregation = 'year';
      chart.updateOptions({
        chart: {
          type: 'bar',
        },
        xaxis: {
          labels: {
            format: 'yyyy',
          }
        },
        tooltip: {
          x: {
            format: "yyyy"
          }
        }
      });
      break;
  }
  updateDataBy(aggregation);
}

dayAggregateButton.addEventListener("click", function(){changeActiveTo(dayAggregateButton)});
monthAggregateButton.addEventListener("click", function(){changeActiveTo(monthAggregateButton)});
weekAggregateButton.addEventListener("click", function(){changeActiveTo(weekAggregateButton)});
yearAggregateButton.addEventListener("click", function(){changeActiveTo(yearAggregateButton)});
reloadButton.addEventListener("click", function(){changeActiveTo(reloadButton)});
