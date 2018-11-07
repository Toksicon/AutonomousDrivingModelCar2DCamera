<template>
<div class="card">
    <div class="card-header">
        <h5 class="card-title mb-0">{{ title }}</h5>
    </div>
    <div class="card-body">
        <img :src="src" />
    </div>
</div>
</template>

<script>
export default {
    props: {
        title: { type: String, default: '', },
        src: { type: String, required: true, },
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
