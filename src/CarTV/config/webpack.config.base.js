const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: [
        path.resolve(__dirname, '../src/js/app.js'),
        path.resolve(__dirname, '../src/sass/main.scss'),
    ],

    output: {
        filename: 'js/app.js',
        path: path.resolve(__dirname, '../static'),
    },
    
    devtool: "source-map",

    resolve: {
        extensions: ['.js', '.json', '.vue'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
        }
    },

    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {   // translates CSS into CommonJS
                        loader: 'css-loader',
                        options: {
                            url: false  // disable url() handling
                        },
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            indent: 'postcss',
                            sourceMap: true,
                            plugins: (loader) => [
                                require('postcss-preset-env')(),
                                require('cssnano')()
                            ],
                        },
                    },
                    'sass-loader',  // compiles SASS to CSS
                ],
            },
            {
                enforce: "pre",
                test: /\.js$/,
                loader: 'source-map-loader',
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                  loaders: {
                    // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
                    // the "scss" and "sass" values for the lang attribute to the right configs here.
                    // other preprocessors should work out of the box, no loader config like this necessary.
                    'scss': [
                      'vue-style-loader',
                      'css-loader',
                      'sass-loader'
                    ],
                    'sass': [
                      'vue-style-loader',
                      'css-loader',
                      'sass-loader?indentedSyntax'
                    ]
                  },
                  // other vue-loader options go here
                },
            },
        ],
    },

    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/main.css',
        }),
        new CopyWebpackPlugin([
            {
                from: path.resolve(__dirname, '../src/static'),
                to: path.resolve(__dirname, '../static'),
            },
        ]),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
        new VueLoaderPlugin(),
    ],
};