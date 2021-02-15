$(document).ready(function() { //Using jQuery, when the document has loaded, do this -
  $('#rateMe2').mdbRate(); //Initialize the MDB star rating plugin
});

var $stars; //Create an empty value called stars

jQuery(document).ready(function ($) { //Again, when the oage is ready, do the following -
  //Initalize the average star ratings
  $.fn.stars = function() {
    return $(this).each(function() {
        //When the average star rating is created, there are two values, rating and num stars.
        //Get the given rating to display
        const rating = $(this).data("rating");
        //Get the number of stars wanted (This will always be 5)
        const numStars = $(this).data("numStars");
        //Define a full colored star
        const fullStar = '<i class="fas fa-star" style="color: gold;"></i>'.repeat(Math.floor(rating));
        //Define a half colored star
        const halfStar = (rating%1!== 0) ? '<i class="fas fa-star-half-alt" style="color: gold;"></i>': '';
        //Define an empty star
        const noStar = '<i class="far fa-star" style="color: gold;"></i>'.repeat(Math.floor(numStars-rating));
        //Return all of the star values
        $(this).html(`${fullStar}${halfStar}${noStar}`);
    });
  };
  $(function(){
    $('.stars').stars();
    //For each star rating code in the html file, run the stars function
  });
  // Custom whitelist to allow for using HTML tags in popover content
  var myDefaultWhiteList = $.fn.tooltip.Constructor.Default.whiteList
  myDefaultWhiteList.textarea = [];
  myDefaultWhiteList.button = [];
  //Initalize the popover that comes when you hover on a star
  $stars = $('.rate-popover');
  // What happens when you hover on a star
  $stars.on('mouseover', function () {
    // Get the data-index of the star hovered and color tthe current star, as well as all of the stars behind the current one
    var index = parseInt($(this).attr('data-index'), 10)+1;
    //Get the hidden input that controls the star value
    var stars = document.getElementById('rate');
    //Set the value of the hidden input to the data-index
    stars.value = index;
  });


});

function Fonky() {
  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
      this.classList.toggle("active2");
      var content = document.getElementsByClassName("content")[0];
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }
}
function search(field, filter) {
  // Declare variables
  var filter, ul, li, a, i, txtValue;
  ul = document.getElementById("container");
  li = ul.getElementsByClassName('col-md-4');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByClassName(field)[0];
    txtValue = a.textContent || a.innerText;
    if (filter.value === "") {
      li[i].setAttribute("style", "display: ''; max-width: 33.333333%;")
    }
    else if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].setAttribute("style", "display: ''; max-width: 100%;")
    } else {
      li[i].setAttribute("style", "display: none; max-width: 33.333333%;")
    }
  }
}

function starsearch() {
  // Declare variables
  var filter, ul, li, a, i, txtValue;
  filter = document.getElementById("starsearch").value.toUpperCase();
  ul = document.getElementById("container");
  li = ul.getElementsByClassName('col-md-4');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByClassName("star")[0];
    txtValue = a.value;
    if (filter.value == "") {
      li[i].setAttribute("style", "display: ''; max-width: 33.333333%;")
    }
    else if (Number(txtValue.toUpperCase()) >= Number(filter) && (txtValue != "")) {
      li[i].setAttribute("style", "display: ''; max-width: 100%;")
    } else {
      li[i].setAttribute("style", "display: none; max-width: 33.333333%;")
    }
  }
}

function ficsearch() {
  // Declare variables
  var filter, ul, li, a, i, txtValue;
  filter = document.getElementById("ficsearch").value.toUpperCase();
  ul = document.getElementById("container");
  li = ul.getElementsByClassName('col-md-4');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByClassName("ficnonfic")[0];
    txtValue = a.value;
    if (filter == "") {
      li[i].setAttribute("style", "display: ''; max-width: 33.333333%;")
    }
    else if (filter === txtValue.toUpperCase()) {
      li[i].setAttribute("style", "display: ''; max-width: 100%;")
    } else {
      li[i].setAttribute("style", "display: none; max-width: 33.333333%;")
    }
  }
}
