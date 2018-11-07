<script>
import { Line, mixins } from 'vue-chartjs';

export default {
    extends: Line,
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
