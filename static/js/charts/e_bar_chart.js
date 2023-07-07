var chartDom = document.getElementById('e_bar_chart');
        var bar_chart = echarts.init(chartDom);
        var option;

        option = {
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
                    tooltip: {
                        valueFormatter: function (value) {
                            return value;
                        }
                    },
                    data: [2.0, 4.9, 7.0, 23.2, 25.6, 76.7]
                },
                {
                    name: 'IN',
                    type: 'bar',
                    tooltip: {
                        valueFormatter: function (value) {
                            return value;
                        }
                    },
                    data: [2.6, 5.9, 9.0, 26.4, 28.7, 70.7]
                }
            ]
        };

        option && bar_chart.setOption(option);