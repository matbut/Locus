var colorPalette = ['#0000b3', '#0000cc', '#0000e6', '#0000ff', '#1a1aff', '#3333ff', '#4d4dff'];
colorPalette.reverse();

var othersColor = '#B0C4DE';

var optionDonut = {
  chart: {
    type: 'donut',
    height: '260px',
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    pie: {
      donut: {
        size: '70%',
      },
      offsetY: -30,
    },
    stroke: {
      colors: undefined
    }
  },
  colors: colorPalette,
  title: {
    text: '',
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
  },
  series: [],
  labels: [],
  legend: {
    position: 'left',
    offsetY: 60
  }
};

var donut;

$.ajax({
  method: "GET",
  url: '/api/userStats',
  data: {
    resultType: resultType,
  },
  success: function (data) {
    switch (resultType) {
      case 'tweet':
        optionDonut.subtitle.text = 'Unique users';
        break;
      case 'google':
        optionDonut.subtitle.text = 'Unique domains';
        break;
      case 'article':
        optionDonut.subtitle.text = 'Unique domains';
        break;
    }

    optionDonut.series = data.series;
    optionDonut.labels = data.labels;
    optionDonut.title.text = data.users;

    optionDonut.colors = colorPalette.slice(0, data.series.length - 1).concat([othersColor]);

    sparkChart = new ApexCharts(document.querySelector("#donut"), optionDonut).render();

  },
  error: function (errorData) {
    console.error(errorData)
  }
});
