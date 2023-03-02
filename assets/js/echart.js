var ctx = document.getElementById('multiline').getContext('2d');

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Car',
            data: [10, 20, 12, 43, 45, 34, 32, 60],
            borderColor: 'rgba(255, 99, 132, 0.5)',
            // backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: false
        }, {
            label: 'Bus',
            data: [1, 2, 1, 4, 4, 3, 3, 6],
            borderColor: 'rgba(54, 162, 235, 0.5)',
            // backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: false
        }, {
            label: 'Truck',
            data: [1, 4, 6, 2, 10, 12, 8, 8],
            borderColor: 'rgba(255, 206, 86, 0.5)',
            // backgroundColor: 'rgba(255, 206, 86, 0.2)',
            fill: false
        }, {
            label: 'Bike',
            data: [30, 40, 27, 43, 45, 40, 62, 20],
            borderColor: 'rgba(75, 192, 192, 0.5)',
            // backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false
        }, {
            label: 'Rickshaw',
            data: [10, 15, 53, 24, 44, 42, 31, 50],
            borderColor: 'rgba(153, 102, 255, 0.5)',
            // backgroundColor: 'rgba(153, 102, 255, 0.2)',
            fill: false
        }, {
            label: 'Van',
            data: [30, 2, 33, 53, 5, 33, 36, 40],
            borderColor: 'rgba(255, 159, 64, 0.5)',
            // backgroundColor: 'rgba(255, 159, 64, 0.2)',
            fill: false
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }],
            xAxes: [{
                type: 'category',
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
            }]
        }
    }
});



// var chartDom = document.getElementById('echartLine');
// var chartDom1 = document.getElementById('echartLine1');
// var chartDom2 = document.getElementById('echartLine2');
// var myChart = echarts.init(chartDom);
// var myChart1 = echarts.init(chartDom1);
// var myChart2 = echarts.init(chartDom2);
// var option;

// const colors = ['#5470C6', '#EE6666'];
// option = {
//   color: colors,
//   tooltip: {
//     trigger: 'none',
//     axisPointer: {
//       type: 'cross'
//     }
//   },
//   legend: {},
//   grid: {
//     top: 70,
//     bottom: 50
//   },
//   xAxis: [
//     {
//       type: 'category',
//       axisTick: {
//         alignWithLabel: true
//       },
//       axisLine: {
//         onZero: false,
//         lineStyle: {
//           color: colors[1]
//         }
//       },
//       axisPointer: {
//         label: {
//           formatter: function (params) {
//             return (
//               'Precipitation  ' +
//               params.value +
//               (params.seriesData.length ? '：' + params.seriesData[0].data : '')
//             );
//           }
//         }
//       },
//       // prettier-ignore
//       data: ['9:00:00', '10:00:00', '11:00:00', '12:00:00']
//     },
//     {
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
//       data: ['9:00:00', '10:00:00', '11:00:00', '12:00:00']
//     }
//   ],
//   yAxis: [
//     {
//       type: 'value'
//     }
//   ],
//   series: [
//     {
//       name: 'Yesterday',
//       type: 'line',
//       xAxisIndex: 1,
//       smooth: true,
//       emphasis: {
//         focus: 'series'
//       },
//       data: [2.6, 5.9, 9.0, 26.4]
//     },
//     {
//       name: 'Today',
//       type: 'line',
//       smooth: true,
//       emphasis: {
//         focus: 'series'
//       },
//       data: [3.9, 5.9, 11.1, 18.7]
//     }
//   ]
// };
// option && myChart.setOption(option);
// option && myChart1.setOption(option);
// option && myChart2.setOption(option);



// bar chart
// var chartDombar = document.getElementById('echartbar');
// var myChartbar = echarts.init(chartDombar);
// var option;

// option = {
//   legend: {},
//   tooltip: {},
//   dataset: {
//     source: [
//       // ['Time', '9:00 AM', '10:00 AM', '12:00 PM','1:00 PM','2:00 PM','3:00 PM'],
//       ['Time', 'Car', 'Bike', 'Rickshaw','Bus','Van','Truck'],
//       ['1/2/23', 43.3, 85.8, 93.7,45,53,56],
//       ['2/2/23', 83.1, 73.4, 55.1,23,45,43],
//       ['3/2/23', 86.4, 65.2, 82.5,67,23,34],
//       ['4/2/23', 72.4, 53.9, 39.1,3,5,6],
//       ['5/2/23', 86.4, 65.2, 82.5,7,3,5],
//       ['6/2/23', 72.4, 53.9, 39.1,8,4,3]
//     ]
//   },
//   xAxis: { type: 'category' },
//   yAxis: {},
//   // Declare several bar series, each will be mapped
//   // to a column of dataset.source by default.
//   series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }, { type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
// };

// option && myChartbar.setOption(option);


var app = {};

var chartDom = document.getElementById('echartbar');
var myChart = echarts.init(chartDom);
var option;

const posList = [
  'left',
  'right',
  'top',
  'bottom',
  'inside',
  'insideTop',
  'insideLeft',
  'insideRight',
  'insideBottom',
  'insideTopLeft',
  'insideTopRight',
  'insideBottomLeft',
  'insideBottomRight'
];
app.configParameters = {
  rotate: {
    min: -90,
    max: 90
  },
  align: {
    options: {
      left: 'left',
      center: 'center',
      right: 'right'
    }
  },
  verticalAlign: {
    options: {
      top: 'top',
      middle: 'middle',
      bottom: 'bottom'
    }
  },
  position: {
    options: posList.reduce(function (map, pos) {
      map[pos] = pos;
      return map;
    }, {})
  },
  distance: {
    min: 0,
    max: 100
  }
};
app.config = {
  rotate: 90,
  align: 'left',
  verticalAlign: 'middle',
  position: 'insideBottom',
  distance: 15,
  onChange: function () {
    const labelOption = {
      rotate: app.config.rotate,
      align: app.config.align,
      verticalAlign: app.config.verticalAlign,
      position: app.config.position,
      distance: app.config.distance
    };
    myChart.setOption({
      series: [
        {
          label: labelOption
        },
        {
          label: labelOption
        },
        {
          label: labelOption
        },
        {
          label: labelOption
        }
      ]
    });
  }
};
const labelOption = {
  show: true,
  position: app.config.position,
  distance: app.config.distance,
  align: app.config.align,
  verticalAlign: app.config.verticalAlign,
  rotate: app.config.rotate,
  formatter: '{c}  {name|{a}}',
  fontSize: 16,
  rich: {
    name: {}
  }
};
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    data: ['Car', 'Bike', 'Rickshaw', 'Bus', 'Van', 'Truck']
  },
  toolbox: {
    show: true,
    orient: 'vertical',
    left: 'right',
    top: 'center',
    feature: {
      mark: { show: true },
      dataView: { show: true, readOnly: false },
      magicType: { show: true, type: ['line', 'bar', 'stack'] },
      restore: { show: true },
      saveAsImage: { show: true }
    }
  },
  xAxis: [
    {
      type: 'category',
      axisTick: { show: false },
      data: ['1/2/23', '2/2/23', '3/2/23', '4/2/23', '5/2/23', '6/2/23']
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: 'Car',
      type: 'bar',
      barGap: 0,
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: [43.3, 83.1, 86.4, 72.4, 86.4, 72.4]
    },
    {
      name: 'Bike',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: [85.8, 73.4, 65.2, 53.9, 65.2, 53.9]
    },
    {
      name: 'Rickshaw',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: [93.7, 55.1, 82.5, 39.1, 82.5, 39.1]
    },
    {
      name: 'Bus',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: [45, 23, 67, 3, 7, 8]
    },
    {
      name: 'Van',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: [53, 45, 23, 5, 3, 4]
    },
    {
      name: 'Truck',
      type: 'bar',
      label: labelOption,
      emphasis: {
        focus: 'series'
      },
      data: [56, 67, 34, 6, 5, 3]
    }
    


      
  ]
};

option && myChart.setOption(option);
