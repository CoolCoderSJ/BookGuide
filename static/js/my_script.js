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
		const fullStar = '<i class="fas fa-star"></i>'.repeat(Math.floor(rating));
		//Define a half colored star
		const halfStar = (rating%1!== 0) ? '<i class="fas fa-star-half-alt"></i>': '';
		//Define an empty star
		const noStar = '<i class="far fa-star"></i>'.repeat(Math.floor(numStars-rating));
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


// Function for searching
function search(field, filter) {
	console.log(filter)
  // Declare variables
  var ul, li, a, i, txtValue;
  ul = document.getElementById("container");
  li = ul.getElementsByClassName('col-md-4');

  // Loop through all list items, and hide those who don't match the search query
  count = 0;
  for (i = 0; i < li.length; i++) {
	a = li[i].getElementsByClassName(field)[0];
	txtValue = a.textContent || a.innerText;
	if (filter === '') {
	  li[i].setAttribute("style", "display: 'block'; max-width: 33.333333%;")
	}
	else if (txtValue.toUpperCase().indexOf(filter) > -1 && li[i].style.display != 'none') {
	  li[i].setAttribute("style", "display: 'block'; max-width: 100%;")
	  count += 1;
	} else {
	  li[i].setAttribute("style", "display: none; max-width: 33.333333%;")
	}
  }
  updatecount(count);
}


function updatecount(val) {
  elem = document.getElementById("bookcount");
  if (val != 0) {
  elem.innerHTML = "Books Found: "+val;
}
else {
	elem.innerHTML = "Showing all Books"
}
}

//What to do when contact form is Filled
function sendMail() {
	document.getElementById('contactform').action="mailto:shuchir.jain@gmail.com?subject=BookGuide Contact Form&body=Sender: "+document.getElementById('name').value+"%0d%0a%0d%0a%0d%0aContent:%0d%0a"+document.getElementById('content').value;
	document.getElementById('contactform').submit();
}

//Change filtertext (Clear Filter/Refilter) if a filter is reselected
function refilter() {
	grade_search = document.getElementById('grade_search')
	genre_search = document.getElementById('genre_search')
	ficsearch = document.getElementById('ficsearch')
	starsearch = document.getElementById('starsearch')
	sort = document.getElementById('sort')
	if (grade_search.value != "" || genre_search.value != "" || ficsearch.value != "" || starsearch.value != "" || sort.value != "new") {
		if (document.getElementById('filtertext').innerHTML === "Clear Filters") {
		document.getElementById('filtertext').innerHTML = "Refilter"
	}
	}
	else {
		document.getElementById('filtertext').innerHTML = "Clear Filters"
	}
}
