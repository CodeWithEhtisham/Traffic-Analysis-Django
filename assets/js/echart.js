var chartDom = document.getElementById('echartLine');
var chartDom1 = document.getElementById('echartLine1');
var chartDom2 = document.getElementById('echartLine2');
var myChart = echarts.init(chartDom);
var myChart1 = echarts.init(chartDom1);
var myChart2 = echarts.init(chartDom2);
var option;

const colors = ['#5470C6', '#EE6666'];
option = {
  color: colors,
  tooltip: {
    trigger: 'none',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {},
  grid: {
    top: 70,
    bottom: 50
  },
  xAxis: [
    {
      type: 'category',
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {
        onZero: false,
        lineStyle: {
          color: colors[1]
        }
      },
      axisPointer: {
        label: {
          formatter: function (params) {
            return (
              'Precipitation  ' +
              params.value +
              (params.seriesData.length ? '：' + params.seriesData[0].data : '')
            );
          }
        }
      },
      // prettier-ignore
      data: ['9:00:00', '10:00:00', '11:00:00', '12:00:00']
    },
    {
    //   type: 'category',
    //   axisTick: {
    //     alignWithLabel: true
    //   },
    //   axisLine: {
    //     onZero: false,
    //     lineStyle: {
    //       color: colors[0]
    //     }
    //   },
    //   axisPointer: {
    //     label: {
    //       formatter: function (params) {
    //         return (
    //           'Precipitation  ' +
    //           params.value +
    //           (params.seriesData.length ? '：' + params.seriesData[0].data : '')
    //         );
    //       }
    //     }
    //   },
      // prettier-ignore
      data: ['9:00:00', '10:00:00', '11:00:00', '12:00:00']
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: 'Yesterday',
      type: 'line',
      xAxisIndex: 1,
      smooth: true,
      emphasis: {
        focus: 'series'
      },
      data: [2.6, 5.9, 9.0, 26.4]
    },
    {
      name: 'Today',
      type: 'line',
      smooth: true,
      emphasis: {
        focus: 'series'
      },
      data: [3.9, 5.9, 11.1, 18.7]
    }
  ]
};
option && myChart.setOption(option);
option && myChart1.setOption(option);
option && myChart2.setOption(option);



// bar chart
var chartDombar = document.getElementById('echartbar');
var myChartbar = echarts.init(chartDombar);
var option;

option = {
  legend: {},
  tooltip: {},
  dataset: {
    source: [
      ['product', '2015', '2016', '2017'],
      ['Matcha Latte', 43.3, 85.8, 93.7],
      ['Milk Tea', 83.1, 73.4, 55.1],
      ['Cheese Cocoa', 86.4, 65.2, 82.5],
      ['Walnut Brownie', 72.4, 53.9, 39.1]
    ]
  },
  xAxis: { type: 'category' },
  yAxis: {},
  // Declare several bar series, each will be mapped
  // to a column of dataset.source by default.
  series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
};

option && myChartbar.setOption(option);