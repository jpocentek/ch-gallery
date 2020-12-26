import 'bootstrap';
import $ from 'jquery';

import '../sass/style.scss';

var $pswp = $('.pswp')[0];
var image = [];

function extractImageData($el) {
  var $linkEl = $el.find('a').first(),
    size = $linkEl.data('size').split('x');

  return {
    src: $linkEl.attr('href'),
    msrc: $linkEl.find('img').first().attr('src'),
    w: parseInt(size[0], 10),
    h: parseInt(size[1], 10)
  };
}

$('.gallery').find('figure').each(function() {
  console.log(extractImageData($(this)));
});
