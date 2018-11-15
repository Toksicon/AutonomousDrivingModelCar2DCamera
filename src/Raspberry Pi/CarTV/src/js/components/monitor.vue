<template>
<div>
    <div class="row">
        <div class="col-12">
            <div class="card flex-fill w-100">
                <div class="card-header">
                    <h5 class="card-title mb-0">Viewport</h5>
                </div>
                <div class="card-body px-4">
                    <viewport-component />
                </div>
            </div>
        </div>
    </div>
    <br>
    <div class="row">
        <div class="col-12">
            <div class="card flex-fill w-100">
                <div class="card-header">
                    <h5 class="card-title mb-0">CAN Logger</h5>
                </div>
                <div class="card-body px-4">
                    <can-component />
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import CanComponent from './monitor/can.vue';
import ViewportComponent from './monitor/viewport.vue';

export default {
    components: {
        CanComponent,
        ViewportComponent,
    },
};
</script>

<style lang="sass" scoped>
</style>
