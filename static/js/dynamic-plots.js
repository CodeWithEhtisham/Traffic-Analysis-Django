var ctx = document.getElementById('multiline').getContext('2d');

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Car',
            data: [],
            borderColor: 'rgba(255, 99, 132, 0.5)',
            // backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: false
        }, {
            label: 'Bus',
            data: [],
            borderColor: 'rgba(54, 162, 235, 0.5)',
            // backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: false
        }, {
            label: 'Truck',
            data: [],
            borderColor: 'rgba(255, 206, 86, 0.5)',
            // backgroundColor: 'rgba(255, 206, 86, 0.2)',
            fill: false
        }, {
            label: 'Bike',
            data: [],
            borderColor: 'rgba(75, 192, 192, 0.5)',
            // backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false
        }, {
            label: 'Rickshaw',
            data: [],
            borderColor: 'rgba(153, 102, 255, 0.5)',
            // backgroundColor: 'rgba(153, 102, 255, 0.2)',
            fill: false
        }, {
            label: 'Van',
            data: [],
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
                labels: []
            }]
        }
    }
});

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

var options = {
    chart: {
        type: 'bar',
        height: '320',
        parentHeightOffset: 0
    },
    colors: ["#f77eb9"],
    grid: {
        borderColor: "rgba(77, 138, 240, .1)",
        padding: {
            bottom: -6
        }
    },
    series: [{
        name: 'sales',
        data: [200, 150, 10, 4, 5, 200]
    }],
    xaxis: {
        // type: 'datetime',
        categories: ['Car', "Rickshaw", "Bus", "Van", "Truck", "Motorcycle"]
    }
}
var apexBarChart = new ApexCharts(document.querySelector("#apexBar"), options);
$(function () {
    'use strict';

    apexBarChart.render();

    if ($('#chartjsArea').length) {
        new Chart($('#chartjsArea'), {
            type: 'line',
            data: {
                // lable must be an array of time series data
                labels: [
                    "00:03:00", "00:06:00", "00:09:00", "00:12:00", "00:15:00", "00:18:00", "00:21:00", "00:24:00", "00:27:00", "00:30:00", "00:33:00", "00:36:00", "00:39:00", "00:42:00", "00:45:00", "00:48:00", "00:51:00", "00:54:00", "00:57:00", "01:00:00"],
                datasets: [{
                    data: [10, 6, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 66, 70],
                    label: "Traffic flow",
                    borderColor: "#f77eb9",
                    backgroundColor: "#ffbedd",
                    fill: true,
                    // LINE LITTLE BIT CURVE
                    lineTension: 0.3,

                }
                ]
            }
        });
    }

});


setInterval(function () {
    $.ajax({
        method: "GET",
        url: "/apis/get_image_objects",
        success: function (data) {
            // Line Chart Data
            var lineCarData = [];
            var lineBusData = [];
            var lineTruckData = [];
            var lineBikeData = [];
            var lineRickshawData = [];
            var lineVanData = [];
            var lineDateLabels = [];



            data.forEach(item => {
                var date = new Date(item.timestamp);
                lineDateLabels.push(date.toLocaleTimeString());
                item.objects.forEach(obj => {
                    switch (obj.label) {
                        case 'car':
                            lineCarData.push(obj.confidence);
                            break;
                        case 'bus':
                            lineBusData.push(obj.confidence);
                            break;
                        case 'truck':
                            lineTruckData.push(obj.confidence);
                            break;
                        case 'bike':
                            lineBikeData.push(obj.confidence);
                            break;
                        case 'rickshaw':
                            lineRickshawData.push(obj.confidence);
                            break;
                        case 'van':
                            lineVanData.push(obj.confidence);
                            break;
                    }
                });
            });

            // Update Line Chart Data
            chart.data.datasets[0].data = lineCarData;
            chart.data.datasets[1].data = lineBusData;
            chart.data.datasets[2].data = lineTruckData;
            chart.data.datasets[3].data = lineBikeData;
            chart.data.datasets[4].data = lineRickshawData;
            chart.data.datasets[5].data = lineVanData;
            chart.options.scales.xAxes[0].labels = lineDateLabels;
            chart.update();
            apexBarChart.updateSeries([{ data: [lineCarData.length,lineBusData.length,lineTruckData.length,lineBikeData.length,lineRickshawData.length,lineVanData.length]}])
            apexBarChart.update()
        },
        error: function () {
            console.log("Error on getting data");
        }
    });
}, 10000); // 10 seconds in milliseconds
