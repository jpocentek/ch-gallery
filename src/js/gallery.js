import $ from 'jquery';

const pswp = $('.pswp')[0];
const items = [];

// Parse single 'a' element and get image information
function extractImageData($el) {
  let $linkEl = $el.find('a').first(),
    size = $linkEl.data('size').split('x');

  return {
    src: $linkEl.attr('href'),
    msrc: $linkEl.find('img').first().attr('src'),
    title: $linkEl.parent('figure').find('figcaption').text(),
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
  const hash = window.location.hash.substring(1);
  let params = {},
    vars;

  if (hash.length < 5) {
    return params;
  }

  vars = hash.split('&');
  for (let i = 0; i < vars.length; i++) {
    if (!vars[i]) {
      continue;
    }
    let pair = vars[i].split('=');
    if (pair.length < 2) {
      continue;
    }
    params[pair[0]] = pair[1];
  }

  if (params.gid) {
    params.gid = parseInt(params.gid, 10);
  }

  if (params.pid) {
    params.pid = parseInt(params.pid, 10);
  }

  return params;
}

function openPhotoSwipe(index) {
  let options = { index: index };
  /* eslint-disable no-undef */
  let gallery = new PhotoSwipe(pswp, PhotoSwipeUI_Default, items, options);
  /* eslint-enable no-undef */
  gallery.init();
}

// Initialize gallery when user click on image.
function onThumbnailClick(e) {
  e.preventDefault();
  openPhotoSwipe($(e.currentTarget).data('index'));
}

function initGallery() {
  getItems();

  // Bind click event to thumbnails
  $('.gallery').find('a').each(function() {
    $(this).on('click', onThumbnailClick);
  });

  // Get params from url if user navigate directly
  // to selected picture
  const hashData = photoswipeParseHash();
  if (hashData.gid && hashData.pid) {
    openPhotoSwipe(hashData.pid - 1);
  }
}

$(document).ready(initGallery);
