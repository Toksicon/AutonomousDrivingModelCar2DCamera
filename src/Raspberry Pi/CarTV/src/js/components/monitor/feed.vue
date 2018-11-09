<template>
<div class="card">
    <div class="card-header">
        <h5 class="card-title mb-0">{{ title }}</h5>
    </div>
    <div class="card-body">
        <img :src="imageSource" ref="img" />
    </div>
</div>
</template>

<script>
export default {
    props: {
        title: { type: String, default: '', },
        src: { type: String, required: true, },
    },

    data() {
        return {
            lastOnLoad: 0,
            imageSource: this.src,
        };
    },

    methods: {
        now() {
            return ((new Date()).getTime());
        }
    },

    mounted() {
        this.$refs.img.addEventListener('load', (e) => {
            this.lastOnLoad = this.now();
        });

        setInterval(() => {
            if ((this.lastOnLoad != 0) && (this.lastOnLoad < (this.now() - 1000))) {
                this.imageSource = this.src + '?t=' + this.now();
            }
        }, 1000);
    },
};
</script>

<style lang="sass" scoped>

.card {
    margin: 10px 15px;

    .card-body {
        padding: 0;

        img {
            margin: 0 -1px;
        }
    }
}

</style>
