<template>
<div>
    <div class="row">
        <feed-component v-for="(feed, index) in feeds" :key="index"
            :title="feed.title"
            :src="feed.src" />
    </div>
</div>
</template>

<script>
import FeedComponent from './feed.vue';

export default {
    components: {
        FeedComponent,
    },

    data() {
        return {
            feeds: [
                {
                    title: 'Captured Image',
                    src: '/video_feed/captured_image',
                }, {
                    title: 'Grayscaled Image',
                    src: '/video_feed/grayscaled_image',
                }, {
                    title: 'Edge Detected Image',
                    src: '/video_feed/edge_detected_image_with_info',
                }
            ]
        };
    },
};
</script>

<style lang="sass" scoped>
</style>
