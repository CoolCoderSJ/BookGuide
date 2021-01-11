$(document).ready(function() {
  $('#rateMe2').mdbRate();
});

var $stars;
jQuery(document).ready(function ($) {
    //$('[data-toggle="tooltip"]').tooltip();

//   function verifyexistingbook(){
//   $('#title').tooltip({ trigger: 'hover', title: 'Test Tooltip' });
//   return false;
// }
  $.fn.stars = function() {
    return $(this).each(function() {
        const rating = $(this).data("rating");
        const numStars = $(this).data("numStars");
        const fullStar = '<i class="fas fa-star" style="color: gold;"></i>'.repeat(Math.floor(rating));
        const halfStar = (rating%1!== 0) ? '<i class="fas fa-star-half-alt" style="color: gold;"></i>': '';
        const noStar = '<i class="far fa-star" style="color: gold;"></i>'.repeat(Math.floor(numStars-rating));
        $(this).html(`${fullStar}${halfStar}${noStar}`);
    });
};
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
});

function myFunc(){
    var star = document.getElementById("rate")
    var desc = document.getElementById("reviewdesc")
    if (star.value === "0" && desc.value === "") {
       desc.setAttribute("class", "form-control border border-danger");
      desc.setAttribute("title", "Either fill in the stars or enter a text review.");
   $('#reviewdesc').tooltip();
    }
    else {
    var frm = document.getElementsByName('addform')[0];
    frm.submit(); // Submit the form
    frm.reset();  // Reset all form data
    return false; // Prevent page refresh
  }
  }
function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}
function verifyexistingbook(allbooks, thebook) {
  allbooks3 = decodeHtml(allbooks)
  allbooks4 = allbooks3.split(",")
  allbooks2 = [];
  bLen = allbooks4.length;
  thebook1 = " '"+thebook+"'"

  for (i = 0; i < bLen; i++){
    if (i==0){
      var str3 = allbooks4[i].split("[")[-1]
      var str = "'"+str3
    allbooks2.push(str.toLowerCase())
    }
    else if(i==bLen-1) {
      var str1 = allbooks4[i].split("]")[-1]
      var str = "'"+str1
      allbooks2.push(str.toLowerCase())
    }
    else {
    var str = allbooks4[i]
    allbooks2.push(str.toLowerCase())
  }

  }
      //$('[data-toggle="tooltip"]').tooltip();
  // document.getElementById("title").setAttribute("data-toggle", "tooltip")
  if (allbooks2.includes(thebook1)){
    document.getElementById("title").setAttribute("class", "form-control border border-danger");
document.getElementById("title").setAttribute("title", "This book already exists.");
   $('#title').tooltip();  }
   else if (document.getElementById("grade").value === ""){
    document.getElementById("grade").setAttribute("class", "custom-select border border-danger");
document.getElementById("grade").setAttribute("title", "Please Select an Item");
   $('#grade').tooltip();  }
   else if (document.getElementById("grade").value === null){
    document.getElementById("grade").setAttribute("class", "custom-select border border-danger");
document.getElementById("grade").setAttribute("title", "Please Select an Item");
   $('#grade').tooltip();  }
   
   else {
    var frm = document.getElementById('newbook');
    frm.submit(); // Submit the form
    frm.reset();  // Reset all form data
   }

}
