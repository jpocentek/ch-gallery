import 'bootstrap';
import $ from 'jquery';

import '../sass/style.scss';

var pswp = $('.pswp')[0];
var items = [];

// Parse single 'a' element and get image information
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

// Parse all 'figure' elements to fetch picture information
function getItems() {
  $('.gallery').find('figure').each(function() {
    items.push(extractImageData($(this)));
  });
}

// Parse GET parameters from url to open selected
// image when user enters page.
function photoswipeParseHash() {
  var hash = window.location.hash.substring(1);
    params = {},
    vars;

  if (hash.length < 5) {
    return params;
  }

  vars = hash.split('&');
  for (var i = 0; i < vars.length; i++) {
    if (!vars[i]) {
      continue;
    }
    var pair = vars[i].split('=');
    if (pair.length < 2) {
      continue;
    }
    params[pair[0]] = pair[1];
  }

  if (params.gid) {
    params.gid = parseInt(params.gid, 10);
  }

  return params;
}

// Initialize gallery when user click on image.
function onThumbnailClick(e) {
  e.preventDefault();

  var options = {
    index: $(e.currentTarget).data('index')
  };

  var gallery = new PhotoSwipe(pswp, PhotoSwipeUI_Default, items, options);
  gallery.init();
}

function initGallery() {
  getItems();
  $('.gallery').find('a').each(function() {
    $(this).on('click', onThumbnailClick);
  });
}

$(document).ready(initGallery);
