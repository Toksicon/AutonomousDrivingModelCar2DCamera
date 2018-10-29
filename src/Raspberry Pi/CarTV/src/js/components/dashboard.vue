<template>
<div class="row">
    <div class="col-12 col-md-8 d-flex">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">Monitor</h5>
            </div>
            <div class="card-body">
                <monitor-component />
            </div>
        </div>
    </div>
    <div class="col-12 col-md-4">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">Memory</h5>
            </div>
            <div class="card-body px-4">
                <virtual-memory-component />
            </div>
        </div>
        <br>
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">CPU</h5>
            </div>
            <div class="card-body px-4">
                <cpu-component />
            </div>
        </div>
    </div>
</div>
</template>

<script>
import CpuComponent from './cpu';
import MonitorComponent from './monitor';

import VirtualMemoryComponent from './telemetry/virtual_memory/component.vue';

export default {
    components: {
        CpuComponent,
        MonitorComponent,
        VirtualMemoryComponent,
    },
};
</script>

<style lang="scss" scoped>

</style>