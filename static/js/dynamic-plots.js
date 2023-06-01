var ctx = document.getElementById("multiline").getContext("2d");

var multiline_chart = new Chart(ctx, {
  type: "line",
  data: {
    datasets: [
      {
        label: "Car",
        data: [],
        borderColor: "rgba(255, 99, 132, 0.5)",
        // backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: false,
      },
      {
        label: "Bus",
        data: [],
        borderColor: "rgba(54, 162, 235, 0.5)",
        // backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: false,
      },
      {
        label: "Truck",
        data: [],
        borderColor: "rgba(255, 206, 86, 0.5)",
        // backgroundColor: 'rgba(255, 206, 86, 0.2)',
        fill: false,
      },
      {
        label: "Bike",
        data: [],
        borderColor: "rgba(75, 192, 192, 0.5)",
        // backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
      },
      {
        label: "Rickshaw",
        data: [],
        borderColor: "rgba(153, 102, 255, 0.5)",
        // backgroundColor: 'rgba(153, 102, 255, 0.2)',
        fill: false,
      },
      {
        label: "Van",
        data: [],
        borderColor: "rgba(255, 159, 64, 0.5)",
        // backgroundColor: 'rgba(255, 159, 64, 0.2)',
        fill: false,
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
            // yxes sholud be number only not float
            // precision: 0
          },
        },
      ],
      xAxes: [
        {
          type: "category",
          labels: [],
        },
      ],
    },
  },
});

var app = {};

var chartDom = document.getElementById("echartbar");
var myChart = echarts.init(chartDom);
var option;

const posList = [
  "left",
  "right",
  "top",
  "bottom",
  "inside",
  "insideTop",
  "insideLeft",
  "insideRight",
  "insideBottom",
  "insideTopLeft",
  "insideTopRight",
  "insideBottomLeft",
  "insideBottomRight",
];
app.configParameters = {
  rotate: {
    min: -90,
    max: 90,
  },
  align: {
    options: {
      left: "left",
      center: "center",
      right: "right",
    },
  },
  verticalAlign: {
    options: {
      top: "top",
      middle: "middle",
      bottom: "bottom",
    },
  },
  position: {
    options: posList.reduce(function (map, pos) {
      map[pos] = pos;
      return map;
    }, {}),
  },
  distance: {
    min: 0,
    max: 100,
  },
};
app.config = {
  rotate: 90,
  align: "left",
  verticalAlign: "middle",
  position: "insideBottom",
  distance: 15,
  onChange: function () {
    const labelOption = {
      rotate: app.config.rotate,
      align: app.config.align,
      verticalAlign: app.config.verticalAlign,
      position: app.config.position,
      distance: app.config.distance,
    };
    myChart.setOption({
      series: [
        {
          label: labelOption,
        },
        {
          label: labelOption,
        },
        {
          label: labelOption,
        },
        {
          label: labelOption,
        },
      ],
    });
  },
};
const labelOption = {
  show: true,
  position: app.config.position,
  distance: app.config.distance,
  align: app.config.align,
  verticalAlign: app.config.verticalAlign,
  rotate: app.config.rotate,
  formatter: "{c}  {name|{a}}",
  fontSize: 16,
  rich: {
    name: {},
  },
};
option = {
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  legend: {
    data: ["Car", "Bike", "Rickshaw", "Bus", "Van", "Truck"],
  },
  toolbox: {
    show: true,
    orient: "vertical",
    left: "right",
    top: "center",
    feature: {
      mark: { show: true },
      dataView: { show: true, readOnly: false },
      magicType: { show: true, type: ["line", "bar", "stack"] },
      restore: { show: true },
      saveAsImage: { show: true },
    },
  },
  xAxis: [
    {
      type: "category",
      axisTick: { show: false },
      data: ["1/2/23", "2/2/23", "3/2/23", "4/2/23", "5/2/23", "6/2/23"],
    },
  ],
  yAxis: [
    {
      type: "value",
    },
  ],
  series: [
    {
      name: "Car",
      type: "bar",
      barGap: 0,
      label: labelOption,
      emphasis: {
        focus: "series",
      },
      data: [43.3, 83.1, 86.4, 72.4, 86.4, 72.4],
    },
    {
      name: "Bike",
      type: "bar",
      label: labelOption,
      emphasis: {
        focus: "series",
      },
      data: [85.8, 73.4, 65.2, 53.9, 65.2, 53.9],
    },
    {
      name: "Rickshaw",
      type: "bar",
      label: labelOption,
      emphasis: {
        focus: "series",
      },
      data: [93.7, 55.1, 82.5, 39.1, 82.5, 39.1],
    },
    {
      name: "Bus",
      type: "bar",
      label: labelOption,
      emphasis: {
        focus: "series",
      },
      data: [45, 23, 67, 3, 7, 8],
    },
    {
      name: "Van",
      type: "bar",
      label: labelOption,
      emphasis: {
        focus: "series",
      },
      data: [53, 45, 23, 5, 3, 4],
    },
    {
      name: "Truck",
      type: "bar",
      label: labelOption,
      emphasis: {
        focus: "series",
      },
      data: [56, 67, 34, 6, 5, 3],
    },
  ],
};

option && myChart.setOption(option);

var options = {
  chart: {
    type: "bar",
    height: "320",
    parentHeightOffset: 0,
  },
  colors: ["#f77eb9"],
  grid: {
    borderColor: "rgba(77, 138, 240, .1)",
    padding: {
      bottom: -6,
    },
  },
  series: [
    {
      name: "sales",
      data: [200, 150, 10, 4, 5, 200],
    },
  ],
  xaxis: {
    // type: 'datetime',
    categories: ["Car", "Rickshaw", "Bus", "Van", "Truck", "Motorcycle"],
  },
};
var apexBarChart = new ApexCharts(document.querySelector("#apexBar"), options);
apexBarChart.render();

var chartarea = new Chart($("#chartjsArea"), {
  type: "line",
  data: {
    labels: [], // Initialize with empty labels
    datasets: [
      // Define your datasets here
    ],
  },
  options: {
    scales: {
      xAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
    },
  },
});

var lineCarData = [];
var lineBusData = [];
var lineTruckData = [];
var lineBikeData = [];
var lineRickshawData = [];
var lineVanData = [];
var lineDateLabels = [];
var lineData = [];
var lineTimestamp = [];

setInterval(function () {
  $.ajax({
    method: "GET",
    url: "/apis/get_image_objects",
    success: function (data) {
      // console.log(data[0])
      // Line Chart Data
      let Car = 0;
      let Bike = 0;
      let Rickshaw = 0;
      let Bus = 0;
      let Van = 0;
      let Truck = 0;
      let time = 0;
      data.forEach((item) => {
        var date = new Date(item.timestamp);
        time = date.toLocaleTimeString();
        lineDateLabels.push(time);
        lineTimestamp.push(time);
        var count = 0;
        item.objects.forEach((obj) => {
          // console.log('acd',count);
          switch (obj.label) {
            case "car":
              Car += 1;
              break;
            case "bus":
              Bus += 1;
              break;
            case "truck":
              Truck += 1;
              break;
            case "bike":
              Bike += 1;
              break;
            case "rickshaw":
              Rickshaw += 1;
              break;
            case "van":
              Van += 1;
              break;
          }
          // total count
          count += 1;
        });
        lineData.push(count);
      });

      // Update Line Chart Data
    //   console.log(Car);
      multiline_chart.data.datasets[0].data.push(Car);
      multiline_chart.data.datasets[1].data.push(Rickshaw);
      multiline_chart.data.datasets[2].data.push(Bus);
      multiline_chart.data.datasets[3].data.push(Van);
      multiline_chart.data.datasets[4].data.push(Truck);
      multiline_chart.data.datasets[5].data.push(Bike);

      multiline_chart.options.scales.xAxes[0].labels.push(time);
      multiline_chart.update();
      apexBarChart.updateSeries([
        {
          data: [
            lineCarData.length,
            lineRickshawData.length,
            lineBusData.length,
            lineVanData.length,
            lineTruckData.length,
            lineBikeData.length,
          ],
        },
      ]);
      apexBarChart.update();

      // fixed line data into 50 length
      if (lineCarData.length > 50) {
        // get last 50 data
        lineData = lineData.slice(Math.max(lineData.length - 50, 1));
        lineTimestamp = lineTimestamp.slice(
          Math.max(lineTimestamp.length - 50, 1)
        );
      }

      // update chartjsArea data
      chartarea.data.labels = lineTimestamp;
      chartarea.data.datasets = [
        {
          data: lineData,
          label: "Traffic flow",
          borderColor: "#f77eb9",
          backgroundColor: "#ffbedd",
          fill: true,
          // LINE LITTLE BIT CURVE
          lineTension: 0.3,
        },
      ];
      chartarea.update();
    },
    error: function () {
      console.log("Error on getting data");
    },
  });
}, 5000); // 10 seconds in milliseconds

const socket = io.connect("http://127.0.0.1:7000");
socket.on("connect", function () {
  console.log("connected");
});

socket.on("disconnect", function () {
  console.log("disconnected");
});

socket.on("prediction_result", function (data) {
  console.log(data);
});
