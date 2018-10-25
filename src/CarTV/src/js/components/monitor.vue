<template>
<div>
    {{ records }}
</div>
</template>

<script>
import { mapState } from 'vuex';

export default {
    props: mapState({
        records: state => state.monitor.records,
        record: state => state.monitor.records[state.monitor.records.length - 1]
    }),

    mounted() {
        console.log(mapState(['monitor.records']).records);
    }
};
</script>
