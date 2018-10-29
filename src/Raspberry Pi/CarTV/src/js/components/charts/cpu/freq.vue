<template>
<div>
    {{ record }}
</div>
</template>

<script>
export default {
    

    computed: {
        record() {
            const records = this.$store.state.cpu_freq.records;

            return ((records.length > 0) ? records[records.length - 1] : null);
        },
    },
};
</script>

