<template>
<div>
    <div>
        <div class="btn-group btn-group-toggle" data-toggle="buttons">
        <label :class="['btn', 'btn-secondary', {'active': !filter}]">
            <input type="radio" name="options" :id="`option`" autocomplete="off" checked @change="test(null)"> All
        </label>
        <label v-for="(f, index) in filters" :key="index"
            :class="['btn', 'btn-secondary', {'active': (f == filter)}]">
            <input type="radio" name="options" :id="`option${index}`" @change="test(f)" autocomplete="off"> {{ f }}
        </label>
        </div>
        <div class="btn-group-toggle" data-toggle="buttons" style="float: right;">
        <label :class="['btn', 'btn-secondary', {'active': autoscroll}]">
            <input type="checkbox" checked v-model="autoscroll"> Autoscroll
        </label>
        </div>
    </div>
    <div class="console" ref="console">
        <div v-for="(message, index) in filteredLog" :key="index">
            <b>[0x{{ message.arbitration_id.toString(16) }}] {{ stringifyArbitration(message.arbitration_id) }}:</b>
            {{ stringifyMessage(message) }}
        </div>
    </div>
</div>
</template>

<script>
const arbitrationIdMapping = {
    0x200: {
        name: 'Sample',
        toObject(payload) {
            return {
                imageId: ((payload[1] << 8) + payload[0]),
                sampleCount: payload[2],
                currentSample: payload[3],
                coord: {
                    x: ((payload[5] << 8) + payload[4]) / Math.pow(2, 16),
                    y: ((payload[7] << 8) + payload[6]) / Math.pow(2, 16),
                },
            };
        },
        toString(object) {
            return  `Image #${object.imageId} [${object.currentSample}/${object.sampleCount}] ` +
                    `(${object.coord.x.toFixed(3)}|${object.coord.y.toFixed(3)})`;
        },
    },
};


export default {
    data() {
        return {
            filter: null,
            autoscroll: true,
            mounted: false,
        };
    },

    computed: {
        log() {
            if (this.autoscroll) {
                this.$nextTick(() => this.scrollToBottom());
            }

            return this.$store.state.can.records;
        },

        filters() {
            let filters = [];

            this.log.forEach((message) => {
                const messageFilter = this.toFilter(message);
                let contained = false;

                filters.forEach((filter) => {
                    if (filter == messageFilter) {
                        contained = true;
                        return;
                    }
                });

                if (!contained) {
                    filters.push(messageFilter);
                }
            });

            return filters;
        },

        filteredLog() {
            if (this.filter == null) {
                return this.log;
            }

            let messages = [];

            this.log.forEach((message) => {
                if (this.filter == this.toFilter(message)) {
                    messages.push(message);
                }
            });

            return messages;
        },
    },

    methods: {
        toFilter(message) {
            return (message.from + ' -> ' + message.to);
        },

        stringifyArbitration(id) {
            return arbitrationIdMapping[id].name;
        },

        stringifyMessage(message) {
            const mapping = arbitrationIdMapping[message.arbitration_id];

            return mapping.toString(mapping.toObject(message.payload));
        },

        scrollToBottom() {
            if (this.mounted) {
                this.$refs.console.scrollTop = this.$refs.console.scrollHeight;
            }
        },

        test(f) { console.error('?'); console.log(f); }
    },

    mounted() {
        this.mounted = true;

        if (this.autoscroll) {
            this.scrollToBottom();
        }
    },
};
</script>

<style lang="sass" scoped>

.console
{
    max-height: 100px;
    overflow: auto;
}

</style>
