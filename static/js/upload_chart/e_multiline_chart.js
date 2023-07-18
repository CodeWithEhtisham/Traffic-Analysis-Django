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

function multi_line_chart_fun(csrfToken,id) {
  // console.log(csrfToken,site_name)
  $.ajax({
      method: "POST",
      url: "/apis/get_multiline_chart_records/uploads/",
      dataType: "json",
      headers: { "X-CSRFToken": csrfToken },
      data: {
          "id": id,
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