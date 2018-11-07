<template>
<div class="row">
    <div class="col-12 col-md-6 d-flex">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">Memory</h5>
            </div>
            <div class="card-body px-4">
                <virtual-memory-component />
            </div>
        </div>
    </div>
    <div class="col-12 col-md-6">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">CPU</h5>
            </div>
            <div class="card-body px-4">
                <cpu-percent-component />
            </div>
        </div>
    </div>
</div>
</template>

<script>
import CpuPercentComponent from './telemetry/cpu_percent/component.vue';
import VirtualMemoryComponent from './telemetry/virtual_memory/component.vue';

export default {
    components: {
        CpuPercentComponent,
        VirtualMemoryComponent,
    },
};
</script>

<style lang="scss" scoped>

</style>