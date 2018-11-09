<template>
<div class="row">
    <div class="col-12 col-md-8 col-xl-9">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">Viewport</h5>
            </div>
            <div class="card-body">
                <viewport-component />
            </div>
        </div>
        <br>
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">CAN Logger</h5>
            </div>
            <div class="card-body">
                <can-component />
            </div>
        </div>
    </div>
    <div class="col-12 col-md-4 col-xl-3">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">CPU</h5>
            </div>
            <div class="card-body px-4">
                <cpu-percent-component />
            </div>
        </div>
        <br>
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">Memory</h5>
            </div>
            <div class="card-body px-4">
                <virtual-memory-component />
            </div>
        </div>
    </div>
</div>
</template>

<script>
import CanComponent from './monitor/can.vue';
import CpuPercentComponent from './telemetry/cpu_percent/component.vue';
import ViewportComponent from './monitor/viewport.vue';

import VirtualMemoryComponent from './telemetry/virtual_memory/component.vue';

export default {
    components: {
        CanComponent,
        CpuPercentComponent,
        ViewportComponent,

        VirtualMemoryComponent,
    },
};
</script>

<style lang="scss" scoped>

</style>