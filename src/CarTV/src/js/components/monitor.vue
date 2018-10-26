<template>
<div class="row">
    <div v-for="(image, index) in images" :key="index" class="image col-md-6">
        <h4>{{ image.name }}</h4>
        <image-component :image-data="image" :points="record.median" />
    </div>
</div>
</template>

<script>
import { mapState } from 'vuex';
import ImageComponent from './monitor/image';

export default {
    components: {
        ImageComponent,
    },

    computed: {
        record() {
            const records = this.$store.state.monitor.records;

            return ((records.length > 0) ? records[records.length - 1] : null);
        },

        images() {
            return this.record ? this.record.images : [];
        }
    },
};
</script>

<style lang="sass" scoped>
div.row {
    margin-bottom: -10px;
}

div.image {
    margin-bottom: 10px;
}
</style>

