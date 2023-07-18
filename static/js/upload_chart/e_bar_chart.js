var chartDom = document.getElementById('e_bar_chart');
var bar_chart = echarts.init(chartDom);
var bar_option;

bar_option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['bar'] },
            restore: { show: true },
            saveAsImage: { show: true }
        }
    },
    legend: {
        data: ['IN', 'OUT']
    },
    xAxis: [
        {
            type: 'category',
            data: ['Car', 'Bike', 'Bus', 'Truck', 'Rickshaw', 'Van'],
            axisPointer: {
                type: 'shadow'
            },
            axisLine: {
                show: false // Hide the x-axis line
            },
            axisTick: {
                show: false // Hide the x-axis tick marks
            },
            splitLine: {
                show: false // Hide the grid lines
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: 'Count',
            min: 0,
            max: 100,
            interval: 5,
            axisLine: {
                show: false // Hide the y-axis line
            },
            axisTick: {
                show: false // Hide the y-axis tick marks
            },
            splitLine: {
                show: false // Hide the grid lines
            }
        }
    ],
    series: [
        {
                name: 'OUT',
                type: 'bar',
                // tooltip: {
                //     valueFormatter: function (value) {
                //         return value;
                //     }
                // },
                data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7]
        },
        {
            name: 'IN',
            type: 'bar',
            // tooltip: {
            //     valueFormatter: function (value) {
            //         return value;
            //     }
            // },
            data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7]
        }
    ]
};

bar_option && bar_chart.setOption(bar_option);



function bar_chart_fun(csrfToken,id) {
    // console.log(csrfToken,site_name)
    $.ajax({
        method: "POST",
        url: "/apis/get_bar_chart_records/upload/",
        dataType: "json",
        headers: { "X-CSRFToken": csrfToken },
        data: {
            "id": id,
        },
        success: function (data) {
            // update the chart with the new data series
            console.log(data)
            bar_option.series = data["data"];
            bar_option.yAxis[0].max = data["max"];
            bar_chart.setOption(bar_option);
  
           
        },
        error: function () {
            console.log("Error on get_vehicle_counts");
        }
    }); 
  
  }