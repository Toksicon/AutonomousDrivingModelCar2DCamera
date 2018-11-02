<template>
<div>
    <canvas ref="img"></canvas>
</div>
</template>

<script>
export default {
    props: ['imageData', 'points'],

    data() {
        return {
            displayOverlay: true,
        };
    },

    watch: {
        imageData() {
            this._updateImage();
        },

        // points() {
        //     this._updateImage();
        // },
    },

    methods: {
        _grayscaleImageData(image, width, height, imageData) {
            let i = 0;
            let offset = 0;
            for (let y = 0; y < height; y++)
            {
                for (let x = 0; x < width; x++)
                {
                    imageData.data[i + 0] = image[offset];  // red
                    imageData.data[i + 1] = image[offset];  // green
                    imageData.data[i + 2] = image[offset];  // blue
                    imageData.data[i + 3] = 255;  // alpha

                    i += 4;
                    offset++;
                }
            }

            return imageData;
        },

        _rgbImageData(image, width, height, imageData) {
            let i = 0;
            let offset = 0;
            for (let y = 0; y < height; y++)
            {
                for (let x = 0; x < width; x++)
                {
                    imageData.data[i + 0] = image[offset];      // red
                    imageData.data[i + 1] = image[offset + 1];  // green
                    imageData.data[i + 2] = image[offset + 2];  // blue
                    imageData.data[i + 3] = 255;                // alpha

                    i += 4;
                    offset += 3;
                }
            }

            return imageData;
        },

        _updateImage() {
            console.warn('update');
            console.time('_updateImage');
            const image = new Uint8Array(this.imageData.data);
            const width = this.imageData.width;
            const height = this.imageData.height;

            const canvas = this.$refs.img;
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            const imageData = ctx.createImageData(width, height);

            if (this.imageData.format == 'rgb') {
                ctx.putImageData(this._rgbImageData(image, width, height, imageData), 0, 0)
            } else if (this.imageData.format == 'grayscale') {
                ctx.putImageData(this._grayscaleImageData(image, width, height, imageData), 0, 0);
            } else {
                console.error('Unknown imageDate format!');
                return;
            }

            //////////////////////////////////////////////////////////////////////////////////
            // draw overlay
            ctx.fillStyle = '#FF0000';
            ctx.strokeStyle = '#FF0000';
            let lastPoint = null;

            this.points.forEach((point) => {
                if (lastPoint) {
                    ctx.beginPath();
                    ctx.moveTo(lastPoint[1], lastPoint[0]);
                    ctx.lineTo(point[1], point[0]);
                    ctx.stroke();
                }

                lastPoint = point;
            });

            this.points.forEach((point) => {
                ctx.fillRect(point[1] - 2, point[0] - 2, 5, 5);
            });

            // this.$refs.img.src = canvas.toDataURL();
            console.timeEnd('_updateImage');

            this.$store.dispatch('monitor/update');
            // this.$emit('rendered_image');
        },
    },

    mounted() {
        this._updateImage();
    },
};
</script>

<style lang="scss" scoped>

div {
    text-align: center;
}

img {
    width: 100%;
    outline: 1px dotted #888;
}

</style>
