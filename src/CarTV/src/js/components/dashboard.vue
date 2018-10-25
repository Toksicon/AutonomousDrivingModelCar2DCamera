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
    <div class="col-12 col-md-4 d-flex">
        <div class="card flex-fill w-100">
            <div class="card-header">
                <h5 class="card-title mb-0">CPU</h5>
            </div>
            <div class="card-body px-4">
                <!-- <cpu-component /> -->
            </div>
        </div>
    </div>
</div>
</template>

<script>
// import CpuComponent from './cpu';
import MonitorComponent from './monitor';

export default {
    components: {
        // CpuComponent,
        MonitorComponent,
    },
};
</script>

<style lang="scss" scoped>

</style>