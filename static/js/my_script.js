$(document).ready(function() {
  $('#rateMe2').mdbRate();
});

var $stars;
jQuery(document).ready(function ($) {
  // Custom whitelist to allow for using HTML tags in popover content
  var myDefaultWhiteList = $.fn.tooltip.Constructor.Default.whiteList
  myDefaultWhiteList.textarea = [];
  myDefaultWhiteList.button = [];
  $stars = $('.rate-popover');
  $stars.on('mouseover', function () {
    var index = parseInt($(this).attr('data-index'), 10)+1;
    var stars = document.getElementById('rate');
    stars.value = index;
  });
});

function myFunc(){
    var frm = document.getElementsByName('addform')[0];
    frm.submit(); // Submit the form
    frm.reset();  // Reset all form data
    return false; // Prevent page refresh
  }