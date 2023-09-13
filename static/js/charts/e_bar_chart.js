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
        
    ]
};

bar_option && bar_chart.setOption(bar_option);



function bar_chart_fun(csrfToken,site_name) {
    // console.log(csrfToken,site_name)
    $.ajax({
        method: "POST",
        url: "/apis/get_bar_chart_records",
        dataType: "json",
        headers: { "X-CSRFToken": csrfToken },
        data: {
            "site_name": site_name,
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