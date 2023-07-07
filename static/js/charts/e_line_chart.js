
var chartDom = document.getElementById('e_line_chart');
var line_chart = echarts.init(chartDom);
var line_option;

setTimeout(function () {
  line_option = {
    legend: {},
    tooltip: {
      trigger: 'axis',
      showContent: true
    },
    dataset: {
      source: [
        ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
        ['IN', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
        ['OUT', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7]
      ]
    },
    xAxis: { type: 'category' },
    yAxis: { gridIndex: 0 },
    grid: { top: '55%' },
    series: [
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'pie',
        id: 'pie',
        radius: '30%',
        center: ['50%', '25%'],
        emphasis: {
          focus: 'self'
        },
        label: {
          formatter: '{b}: Vehicle '
        },
        encode: {
          itemName: 'product',
          value: '2012',
          tooltip: '2012'
        }
      }
    ]
  };
  line_chart.on('updateAxisPointer', function (event) {
    const xAxisInfo = event.axesInfo[0];
    if (xAxisInfo) {
      const dimension = xAxisInfo.value + 1;
      line_chart.setOption({
        series: {
          id: 'pie',
          label: {
            formatter: '{b}: Vehicle'
          },
          encode: {
            value: dimension,
            tooltip: dimension
          }
        }
      });
    }
  });
  line_chart.setOption(line_option);
});

line_option && line_chart.setOption(line_option);
