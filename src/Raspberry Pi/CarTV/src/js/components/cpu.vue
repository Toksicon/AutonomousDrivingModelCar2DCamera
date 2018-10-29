<template>

<cpu-chart :chart-data="chartData" :options="options">
</cpu-chart>

</template>

<script>
import CpuChart from './charts/cpu/freq';

export default {
    components: {
        CpuChart,
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
                            suggestedMax: 4000,
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
            },
            chartData: {
                labels: [],
                datasets: this._datasets(),
            },
        };
    },

    computed: {
        freq_current_list() {
            return this.$store.state.cpu_freq.records.map(
                (record) => record.current
            );
        },

        freq_min_list() {
            return this.$store.state.cpu_freq.records.map(
                (record) => record.min
            );
        },

        freq_max_list() {
            return this.$store.state.cpu_freq.records.map(
                (record) => record.max
            );
        },

        _chartData() {
            let datasets = this._datasets();
            
            return {
                labels: this.freq_current_list.map(_ => null),
                datasets,
            };
        },
    },

    watch: {
        freq_current_list() {
            this.chartData = this._chartData;
        }
    },

    methods: {
        _datasets() {
            return [
                {
                    label: 'current',
                    data: this.freq_current_list ? this.freq_current_list : [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    lineTension: 0.1,
                }, {
                    label: 'max',
                    data: this.freq_max_list ? this.freq_max_list : [],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    lineTension: 0.1,
                }, {
                    label: 'min',
                    data: this.freq_min_list ? this.freq_min_list : [],
                    backgroundColor: 'rgba(255, 205, 86, 0.2)',
                    borderColor: 'rgb(255, 205, 86)',
                    lineTension: 0.1,
                },
            ];
        },
    },
};
</script>