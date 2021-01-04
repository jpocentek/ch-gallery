import $ from 'jquery';

const confirmTxt = 'Are you sure you want to delete this item?';

function protectFormSubmit(e) {
  e.preventDefault();

  if (confirm(confirmTxt)) {
    $(e.currentTarget).parent('form').submit();
  }
}

function init() {
  $('.image-delete-form [type="submit"]')
    .on('click', protectFormSubmit);
}

$(document).ready(init);
