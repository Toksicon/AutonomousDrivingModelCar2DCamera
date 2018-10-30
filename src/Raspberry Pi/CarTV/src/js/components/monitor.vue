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
            return this.$store.state.monitor;
        },

        images() {
            return this.record.images;
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
