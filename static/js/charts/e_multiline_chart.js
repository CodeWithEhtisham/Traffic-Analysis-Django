var chartDom = document.getElementById('e_multiline_chart');
var multi_line_chart = echarts.init(chartDom);
var multiline_options;

multiline_options = {
  title: {
    text: 'Total Count'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Car', 'Bike', 'Bus', 'Truck', 'Rickshaw', 'Van'],
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    data: ['02:32:33', '02:32:33', '02:32:33', '02:32:33', '02:32:33', '02:32:33', '02:32:34', '02:32:34', '02:32:34', '02:32:35', '02:32:35']
  },
  yAxis: {
    type: 'value',
    max: 30,
    min: 0,
    // interval: 1 
  },
  series: [
    {
      name: 'Car',
      type: 'line',
      // stack: 'Total',
      data: [1, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6]

    },
    {
      name: 'Bike',
      type: 'line',
      data: [0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 4, 4]
    },
    {
      name: 'Bus',
      type: 'line',
      data: [0, 0, 0, 0, 0, 0, 0, 0, 1]
    },
    {
      name: 'Truck',
      type: 'line',
      data: [0, 0, 0, 0, 0, 0, 0, 2, 3]
    },
    {
      name: 'Rickshaw',
      type: 'line',
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    {
        name: 'Van',
        type: 'line',

        data: [0, 0, 0, 0, 0, 0, 1, 2, 3]
      }
  ]
};

multiline_options && multi_line_chart.setOption(multiline_options);

function multi_line_chart_fun(csrfToken,site_name) {
  // console.log(csrfToken,site_name)
  $.ajax({
      method: "POST",
      url: "/apis/get_multiline_chart_records",
      dataType: "json",
      headers: { "X-CSRFToken": csrfToken },
      data: {
          "site_name": site_name,
      },
      success: function (data) {
          // update the chart with the new data series
          multiline_options.series = data["data"];
          multiline_options.yAxis.max = data["max"];
          multiline_options.xAxis.data = data["time_stamp"];

          multi_line_chart.setOption(multiline_options);

         
      },
      error: function () {
          console.log("Error on get_vehicle_counts");
      }
  });

}



// import * as echarts from 'echarts';

// var chartDom = document.getElementById('main');
// var myChart = echarts.init(chartDom);
// var option;

// // prettier-ignore
// let timeData = ['2009/10/1 0:00', '2009/10/1 1:00', '2009/10/1 2:00', '2009/10/1 3:00', '2009/10/1 4:00', '2009/10/1 5:00', '2009/10/1 6:00', '2009/10/1 7:00', '2009/10/1 8:00', '2009/10/1 9:00', '2009/10/1 10:00', '2009/10/1 11:00', '2009/10/1 12:00', '2009/10/1 13:00', '2009/10/1 14:00'];
// timeData = timeData.map(function (str) {
//   return str.replace('2009/', '');
// });

// option = {
//   title: {
//     text: 'IN vs OUT',
//     left: 'center'
//   },
//   tooltip: {
//     trigger: 'axis',
//     axisPointer: {
//       animation: false
//     }
//   },
//   legend: {
//     data: ['Car', 'Bike'],
//     left: 10
//   },
//   toolbox: {
//     feature: {
//       dataZoom: {
//         yAxisIndex: 'none'
//       },
//       restore: {},
//       saveAsImage: {}
//     }
//   },
//   axisPointer: {
//     link: [
//       {
//         xAxisIndex: 'all'
//       }
//     ]
//   },
//   dataZoom: [
//     {
//       show: true,
//       realtime: true,
//       start: 30,
//       end: 70,
//       xAxisIndex: [0, 1]
//     },
//     {
//       type: 'inside',
//       realtime: true,
//       start: 30,
//       end: 70,
//       xAxisIndex: [0, 1]
//     }
//   ],
//   grid: [
//     {
//       left: 60,
//       right: 50,
//       height: '35%'
//     },
//     {
//       left: 60,
//       right: 50,
//       top: '55%',
//       height: '35%'
//     }
//   ],
//   xAxis: [
//     {
//       type: 'category',
//       boundaryGap: false,
//       axisLine: { onZero: true },
//       data: timeData
//     },
//     {
//       gridIndex: 1,
//       type: 'category',
//       boundaryGap: false,
//       axisLine: { onZero: true },
//       data: timeData,
//       position: 'top'
//     }
//   ],
//   yAxis: [
//     {
//       name: 'IN',
//       type: 'value',
//       max: 200
//     },
//     {
//       gridIndex: 1,
//       name: 'OUT',
//       type: 'value',
//       inverse: true
//     }
//   ],
//   series: [
//     {
//       name: 'Bike',
//       type: 'line',
//       symbolSize: 8,
//       data: [47, 56, 96, 55, 25, 44, 44, 74, 24, 64, 84, 94, 54, 34, 74]
//     },
//     {
//       name: 'Car',
//       type: 'line',
//       symbolSize: 8,
//       data: [9, 89, 28, 67, 86, 65, 25, 85, 46, 97, 88, 19, 99, 91, 42]
//     },
//     {
//       name: 'Car',
//       type: 'line',
//       xAxisIndex: 1,
//       yAxisIndex: 1,
//       symbolSize: 8,
//       data: [10, 30, 50, 30, 50, 30, 70, 90, 20, 30, 10, 70, 10, 40, 50]
//     },
//     {
//       name: 'Bike',
//       type: 'line',
//       xAxisIndex: 1,
//       yAxisIndex: 1,
//       symbolSize: 8,
//       data: [40, 20, 40, 60, 80, 40, 20, 10, 40, 60, 80, 55, 10, 15, 20]
//     }
//   ]
// };

// option && myChart.setOption(option);
