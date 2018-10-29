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
                tooltips: {
                    callbacks: {
                        label(tooltipItem, data) {
                            return bytesToSize(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]);
                        },
                    },
                },
            },
        };
    },

    computed: {
        record() {
            const r = this.$store.state.virtual_memory.records;            
            return (r.length ? r[r.length - 1] : null);
        },

        total() {
            return this.record ? this.record.total : 0;
        },

        used() {
            return this.record ? (this.record.total - this.record.available) : 0;
        },

        available() {
            return this.record ? this.record.available : 0;
        },

        chartData() {
            return {
                labels: ['Available', 'Used'],
                datasets: [
                    {
                        backgroundColor: ['#00ff00', '#f87979'],
                        data: [this.available, this.used],
                    }
                ]
            };
        }
    },
};
</script>
