const path = require('path');
const ErrorOverlayPlugin = require('error-overlay-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: './src/index.ts',
    devtool: 'inline-source-map',
    mode: 'development',
    output: {
        path: __dirname + '/dist',
        filename: 'index_bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        // Since sass-loader (weirdly) has SCSS as its default parse mode, we map
                        // the "scss" and "sass" values for the lang attribute to the right configs here.
                        // other preprocessors should work out of the box, no loader config like this necessary.
                        'scss': 'vue-style-loader!css-loader!sass-loader',
                        'sass': 'vue-style-loader!css-loader!sass-loader?indentedSyntax',
                    }
                    // other vue-loader options go here
                }
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader"
                ]
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                options: {
                    presets: ['@babel/preset-env']
                }
            },
            {
                test: /\.tsx?$/,
                loader: 'ts-loader',
                exclude: /node_modules/,
                options: {
                    appendTsSuffixTo: [/\.vue$/],
                }
            },
            {
                test: /\.(png|jpg|gif|svg|ttf|woff)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            }
        ]
    },
    resolve: {
        extensions: ['.ts', '.js', '.vue', '.json'],
        alias: {
            '@': path.resolve(__dirname, 'src'),
            'vue$': 'vue/dist/vue.esm.js',
        }
    },
    devServer: {
        host: '0.0.0.0',
        port: 8000,
        historyApiFallback: true,
        disableHostCheck: true, // C9 compatibility
        proxy: {
            "/api": {
                target: "http://localhost:5000",
                pathRewrite: { "^/api" : ""}
            }
        }
    },
    optimization: {
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /node_modules/, // you may add "vendor.js" here if you want to
                    name: "vendor",
                    chunks: "initial",
                    enforce: true
                }
            }
        }
    },
    plugins: [
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: "[name].css",
            chunkFilename: "[id].css"
        }),
        new ErrorOverlayPlugin(),
        new HtmlWebpackPlugin({
            template: 'index.html'
        }),
    ],
};
