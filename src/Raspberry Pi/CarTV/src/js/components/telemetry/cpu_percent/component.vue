<template>
    <chart :chart-data="chartData" :options="options" />
</template>
<script>
import { bytesToSize } from '../../../util';
import Chart from './chart';

export default {
    components: {
        Chart,
    },

    data() {
        return {
            options: {
                fill: true,
                scales: {
                    xAxes: [{
                        display: false,
                    }],
                    yAxes: [{
                        display: true,
                        ticks: {
                            suggestedMin: 0,
                            suggestedMax: 100,
                            beginAtZero: true,
                        }
                    }]
                },
                tooltips: {
                    callbacks: {
                        title: () => '',
                    },
                },
                elements: {
                    line: {
                        tension: 0, // disables bezier curves
                    },
                    point: {
                        radius: 0,  // hide points
                    },
                },
                animation: false,
            },
        };
    },

    computed: {
        chartData() {
            const colors = [{   // blue
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                }, {    // red
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                }, {    // yellow
                    backgroundColor: 'rgba(255, 205, 86, 0.2)',
                    borderColor: 'rgb(255, 205, 86)',
                }, {    // green
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgb(75, 192, 192)',
                }, {    // purple
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgb(153, 102, 255)',
                }, {    // orange
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderColor: 'rgb(255, 159, 64)',
                }, {    // gray
                    backgroundColor: 'rgba(201, 203, 207, 0.2)',
                    borderColor: 'rgb(201, 203, 207)',
                },
            ];

            const records = this.$store.state.cpu_percent.records;
            let dataList = [];
            let labels = [];

            for (const i in records) {
                const record = records[i];
                labels.push(i);

                for (const j in record) {
                    if (!dataList[j]) {
                        dataList[j] = [];
                    }

                    dataList[j][i] = record[j];
                }
            }

            let datasets = [];

            for (const i in dataList) {
                datasets.push({
                    label: 'CPU ' + ((i << 0) + 1),
                    data: dataList[i],
                    ...colors[i % colors.length]
                });
            }

            return {
                labels,
                datasets,
            };
        }
    },
};
</script>
