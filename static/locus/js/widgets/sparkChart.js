Apex.grid = {
  padding: {
    right: 0,
    left: 0
  }
};

Apex.dataLabels = {
  enabled: false
};

var sparkOptions = {
  chart: {
    type: 'area',
    height: 160,
    //width: '100%',
    //height: '100%',
    sparkline: {
      enabled: true
    },
  },
  series: [],
  stroke: {
    curve: 'straight'
  },
  fill: {
    opacity: 1,
  },
  labels: [...Array(24).keys()].map(n => `2018-09-0${n + 1}`),
  yaxis: {
    //min: 0
  },
  xaxis: {
    type: 'datetime',
  },
  colors: ['#008FFB'],
  title: {
    text: 0,
    offsetX: 0,
    style: {
      fontSize: '24px',
      cssClass: 'apexcharts-yaxis-title'
    }
  },
  subtitle: {
    text: '',
    offsetX: 0,
    style: {
      fontSize: '14px',
      cssClass: 'apexcharts-yaxis-title'
    }
  }
};

var sparkChart;

$.ajax({
  method: "GET",
  url: '/api/chart',
  data: {
    aggregate: 'day',
  },
  success: function (data) {
    switch (resultType) {
      case 'tweet':
        sparkOptions.series = [data[0]];
        sparkOptions.subtitle.text = 'Tweets';
        break;
      case 'google':
        sparkOptions.series = [data[1]];
        sparkOptions.subtitle.text = 'Google Results';
        break;
      case 'article':
        sparkOptions.series = [data[2]];
        sparkOptions.subtitle.text = 'Article Results';
        break;
    }
    sparkOptions.title.text = sparkOptions.series[0].data.reduce(function (total, element) {
      return total + element[1];
    }, 0);

    sparkChart = new ApexCharts(document.querySelector("#spark1"), sparkOptions).render();

  },
  error: function (errorData) {
    console.error(errorData)
  }
});