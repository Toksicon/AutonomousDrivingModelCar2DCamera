<template>
<div>
    <img ref="img" />
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

        points() {
            this._updateImage();
        },
    },

    methods: {
        _updateImage() {
            const image = this.imageData.data;
            const width = this.imageData.data[0].length;
            const height = this.imageData.data.length;

            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');

            const imageData = ctx.createImageData(width, height);

            let i = 0;
            for (let y = 0; y < height; y++)
            {
                for (let x = 0; x < width; x++)
                {
                    let rgba = [];

                    if (this.imageData.format == 'grayscale')
                    {
                        const grayscale = image[y][x];
                        rgba = [grayscale, grayscale, grayscale, 255];
                    }
                    else if (this.imageData.format == 'rgb' || this.imageData.format == 'rgba')
                    {
                        rgba = image[y][x];
                        if (rgba.length == 3)
                        {
                            rgba[3] = 255;
                        }
                    }

                    imageData.data[i + 0] = rgba[0];  // red
                    imageData.data[i + 1] = rgba[1];  // green
                    imageData.data[i + 2] = rgba[2];  // blue
                    imageData.data[i + 3] = rgba[3];  // alpha

                    i += 4;
                }
            }

            ctx.putImageData(imageData, 0, 0);

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

            this.$refs.img.src = canvas.toDataURL();
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
