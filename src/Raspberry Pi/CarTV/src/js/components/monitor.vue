<template>
<div>
    <div class="row">
        <feed-component v-for="(feed, index) in feeds" :key="index"
            :title="feed.title"
            :src="feed.src" />
    </div>
    <can-component />
</div>
</template>

<script>
import CanComponent from './monitor/can.vue';
import FeedComponent from './monitor/feed.vue';

export default {
    components: {
        CanComponent,
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
                    src: '/video_feed/edge_detected_image',
                }
            ]
        };
    },
};
</script>

<style lang="sass" scoped>
</style>
