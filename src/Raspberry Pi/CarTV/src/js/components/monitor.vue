<template>
<div class="row">
    <img src="/video_feed" />
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

    data() {
        return {
            renderedImages: 0,
        };
    },

    computed: {
        record() {
            const rec = this.$store.state.monitor;
            this.renderedImages = 0;
            return rec;
        },

        images() {
            return this.record.images;
        },
    },

    mounted() {
        this.$on('rendered_image', () => {
            this.renderedImages++;
            console.log('rendered: ' + this.renderedImages);

            if (this.renderedImages == this.images.length)
            {
                this.$store.dispatch('monitor/update');
            }
        })
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
