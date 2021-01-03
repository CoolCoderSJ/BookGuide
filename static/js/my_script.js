$(document).ready(function() {
  $('#rateMe2').mdbRate();
});

var $stars;
jQuery(document).ready(function ($) {
  function addScore(score, $domElement) {
    $("<span class='stars-container'>")
      .addClass("stars-" + score.toString())
      .text("★★★★★")
      .appendTo($domElement);
  }
  $.fn.stars = function() {
    return $(this).each(function() {
        const rating = $(this).data("rating");
        const numStars = $(this).data("numStars");
        const fullStar = '<i class="fas fa-star" style="color: gold;"></i>'.repeat(Math.floor(rating));
        const halfStar = (rating%1!== 0) ? '<i class="fas fa-star-half-alt" style="color: gold;"></i>': '';
        const noStar = '<i class="far fa-star" style="color: gold;"></i>'.repeat(Math.floor(numStars-rating));
        $(this).html(`${fullStar}${halfStar}${noStar}`);
    });
}
$(function(){
                $('.stars').stars();
            });
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
  addScore(70, $("#fixture"));
});

function myFunc(){
    var frm = document.getElementsByName('addform')[0];
    frm.submit(); // Submit the form
    frm.reset();  // Reset all form data
    return false; // Prevent page refresh
  }

