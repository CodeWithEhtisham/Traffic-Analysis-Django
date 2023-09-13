var chartDom = document.getElementById('e_multiline_chart');
var multi_line_chart = echarts.init(chartDom);
var multiline_options;

let timeData = ['2009/10/1 0:00', '2009/10/1 1:00', '2009/10/1 2:00', '2009/10/1 3:00', '2009/10/1 4:00', '2009/10/1 5:00', '2009/10/1 6:00', '2009/10/1 7:00', '2009/10/1 8:00', '2009/10/1 9:00', '2009/10/1 10:00', '2009/10/1 11:00', '2009/10/1 12:00', '2009/10/1 13:00', '2009/10/1 14:00'];
timeData = timeData.map(function (str) {
  return str;
});

multiline_options = {
  title: {
    text: 'IN vs OUT',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      animation: false
    }
  },
  legend: {
    data: ['Car', 'Bike','Bus','Truck','Rickshaw','Van'],
    left: 10
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  axisPointer: {
    link: [
      {
        xAxisIndex: 'all'
      }
    ]
  },
  dataZoom: [
    {
      show: true,
      realtime: true,
      start: 0,
      end: 100,
      xAxisIndex: [0, 1]
    },
    {
      type: 'inside',
      realtime: true,
      start: 30,
      end: 70,
      xAxisIndex: [0, 1]
    }
  ],
  grid: [
    {
      left: 60,
      right: 50,
      height: '35%'
    },
    {
      left: 60,
      right: 50,
      top: '55%',
      height: '35%'
    }
  ],
  xAxis: [
    {
      type: 'category',
      boundaryGap: false,
      axisLine: { onZero: true },
      data: timeData
    },
    {
      gridIndex: 1,
      type: 'category',
      boundaryGap: false,
      axisLine: { onZero: true },
      data: timeData,
      position: 'top'
    }
  ],
  yAxis: [
    {
      name: 'IN',
      type: 'value',
      max: 20
    },
    {
      gridIndex: 1,
      name: 'OUT',
      type: 'value',
      inverse: true,
      max:25
    }
  ],
  series: [
    
  ]
};
multiline_options && multi_line_chart.setOption(multiline_options);

function multi_line_chart_fun(csrfToken,id) {
  // console.log(csrfToken,site_name)
  $.ajax({
      method: "POST",
      url: "/apis/get_multiline_chart_records_uploads",
      dataType: "json",
      headers: { "X-CSRFToken": csrfToken },
      data: {
          "id": id,
      },
      success: function (data) {
          // update the chart with the new data series
          multiline_options.series = data["data"];
          multiline_options.yAxis[0]['max'] = data["max_in"];
          multiline_options.yAxis[1]['max'] = data["max_out"];
          multiline_options.xAxis[0]['data']=data['time_stamp']
          multiline_options.xAxis[1]['data']=data['time_stamp']

          multi_line_chart.setOption(multiline_options);

         
      },
      error: function () {
          console.log("Error on get_vehicle_counts");
      }
  });

}