<script>
import { Doughnut, mixins } from 'vue-chartjs';

export default {
    extends: Doughnut,
    mixins: [mixins.reactiveProp],

    props: ['chartData', 'options'],

    data() {
        return {
            htmlLegend: null,
        };
    },

    mounted() {
        this.renderChart(this.chartData, this.options);
        this.htmlLegend = this.generateLegend();
    }
};
</script>

