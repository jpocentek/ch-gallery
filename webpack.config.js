const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {

  entry: {
    main: './src/js/main.js',
    gallery: './src/js/gallery.js'
  },

  output: {
    path: path.resolve(__dirname, 'chgallery/static/dist'),
    filename: '[name].js',

    // See: https://stackoverflow.com/questions/64294706/webpack5-automatic-publicpath-is-not-supported-in-this-browser
    publicPath: ''
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          {
            loader: 'css-loader'
          },
          {
            loader: 'postcss-loader'
          },
          {
            loader: 'sass-loader',
            options: {
              implementation: require('sass')
            }
          }
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'images'
            }
          }
        ]
      }
    ]
  },

  plugins: [

    new MiniCssExtractPlugin({
      filename: 'style.css'
    }),

    new webpack.ProvidePlugin({
      PhotoSwipe: 'photoswipe',
      PhotoSwipeUI_Default: 'photoswipe/src/js/ui/photoswipe-ui-default.js'
    })

  ],

  mode: 'development'
};
