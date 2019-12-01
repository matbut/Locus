var aggregation = 'week'

var allData = []

var options = {
  chart: {
    type: 'line',
    stacked: false,
    height: 250,
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
      dataPointSelection: function (e, x, opts) {

        //console.log(allData[opts.seriesIndex]);
        //console.log(allData[opts.seriesIndex].data[opts.dataPointIndex][0]);

        date = allData[opts.seriesIndex].data[opts.dataPointIndex][0];
        type = allData[opts.seriesIndex].name.toLowerCase();

        $.ajax({
          method: "GET",
          url: '/api/data',
          data: {
            date: date,
            type: type,
            aggregation: aggregation,
          },
          success: function (nodes) {
            clearTables()
            for (const node of nodes) {
              addNode(node)
            }
            openTab(type);
          },
          error: function (errorData) {
            console.error(errorData)
          }
        });


      }
    },
  },
  colors: ['#0084b4', '#00b435', '#7b3db4'],
  dataLabels: {
    enabled: false
  },
  series: [],
  markers: {
    size: 4,
    strokeWidth: 0,
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
  yaxis: [
    {
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: '#0084b4'
      },
      labels: {
        style: {
          color: '#0084b4',
        }
      },
    },
    {
      seriesName: 'Google',
      opposite: true,
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: '#00b435'
      },
      labels: {
        style: {
          color: '#00b435',
        }
      },
    },
    {
      seriesName: 'Database',
      opposite: true,
      axisTicks: {
        show: true,
      },
      axisBorder: {
        show: true,
        color: '#7b3db4'
      },
      labels: {
        style: {
          color: '#7b3db4',
        },
      },
    },
  ],
  xaxis: {
    type: 'datetime',
    title: {
      //text: 'Time'
    },
    axisTicks: {
      show: true,
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
      allData = data;
      chart.updateSeries(data, true);

      wholeData = data[0].data.concat(data[1].data).concat(data[2].data);

      barNumber = wholeData.map((a) => Math.sign(a[1])).reduce((a, b) => a + b, 0);

      chart.updateOptions({
        chart: {
          type: barNumber < 30 ? 'bar' : 'line',
        }
      })
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

showTweetButton.addEventListener("click", function () {
  toggleSeries(showTweetButton, "Tweets")
});
showGoogleButton.addEventListener("click", function () {
  toggleSeries(showGoogleButton, "Google")
});
showDatabaseButton.addEventListener("click", function () {
  toggleSeries(showDatabaseButton, "Database")
});

function toggleSeries(checkBox, series) {
  if (checkBox.classList.contains('btn-outline-primary'))
    checkBox.classList.replace('btn-outline-primary', 'btn-primary');
  else
    checkBox.classList.replace('btn-primary', 'btn-outline-primary');

  chart.toggleSeries(series);
  clearTables()
}

reloadButton = document.getElementById("reloadButton")

dayAggregateButton = document.getElementById('dayAggregate');
weekAggregateButton = document.getElementById('weekAggregate');
monthAggregateButton = document.getElementById('monthAggregate');
yearAggregateButton = document.getElementById('yearAggregate');

aggregateButtons = [dayAggregateButton, monthAggregateButton, weekAggregateButton, yearAggregateButton];

function changeActiveTo(clickedButton) {
  clearTables();
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

dayAggregateButton.addEventListener("click", function () {
  changeActiveTo(dayAggregateButton)
});
monthAggregateButton.addEventListener("click", function () {
  changeActiveTo(monthAggregateButton)
});
weekAggregateButton.addEventListener("click", function () {
  changeActiveTo(weekAggregateButton)
});
yearAggregateButton.addEventListener("click", function () {
  changeActiveTo(yearAggregateButton)
});
reloadButton.addEventListener("click", function () {
  changeActiveTo(reloadButton)
});
