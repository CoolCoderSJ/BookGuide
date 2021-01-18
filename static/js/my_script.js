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


//Used to identify whether either a star rating or text rating is given
function myFunc(){
    //Get the html element with id "rate" and set it to a variable, star (This is the star rating)
    var star = document.getElementById("rate")
    //Get the html element with id "reviewdesc" and set it to a variable, desc (This is the text review)
    var desc = document.getElementById("reviewdesc")
    //If both the star rating and text are empty, do -
    if (star.value === "0" && desc.value === "") {
      // Highlight the text box in red
       desc.setAttribute("class", "form-control border border-danger");
       //Show a tooltip asking the user to either fill in the text or star rating
      desc.setAttribute("title", "Either fill in the stars or enter a text review.");
      // Activate the tooltip
      $('#reviewdesc').tooltip();
    }
    //If either one is filled in...
    else {
      var frm = document.getElementsByName('addform')[0];
      frm.submit(); // Submit the form
      frm.reset();  // Reset all form data
    }
}

//This is used to decode HTML codes, for example - &quot; is a quotation mark
function decodeHtml(html) {
  //Create an element whose value is the decoded html
    var txt = document.createElement("textarea");
    //Set the element to the html given
    txt.innerHTML = html;
    //return the value of the html
    return txt.value;
}

//This function checks to make sure that the book is not already in the database
function verifyexistingbook(allbooks, thebook) {
  //Decode html from the database book titles
  allbooks3 = decodeHtml(allbooks)
  //Passing a python list to javascript makes it a string, so we have to convert it to a js array
  allbooks4 = allbooks3.split(",")
  //This will be used to lower titles
  allbooks2 = [];
  //Get num of books
  bLen = allbooks4.length;
  //There are some issues converting python lists to js arrays, so convert inputted title "thebook", to a title with quotes around it
  thebook1 = " '"+thebook+"'"
  //Do the following for each book in the array
  for (i = 0; i < bLen; i++){
    //If the book is the first book...
    if (i==0){
      //Remove the "[" that comes when converting
      var str3 = allbooks4[i].split("[")[-1]
      var str = "'"+str3
      //Add the final result to the list of processed books
      allbooks2.push(str.toLowerCase())
    }
    //If its the last book...
    else if(i==bLen-1) {
      //Remove the "]" that comes when converting
      var str1 = allbooks4[i].split("]")[-1]
      var str = "'"+str1
      //add to the list of processed books
      allbooks2.push(str.toLowerCase())
    }
    //Otherwise...
    else {
      var str = allbooks4[i]
      //Add to the list of processed books
      allbooks2.push(str.toLowerCase())
  }

  }
  //If book already exists...
  if (allbooks2.includes(thebook1)){
    //Highlight the title box in red
    document.getElementById("title").setAttribute("class", "form-control border border-danger");
    //Set the content of the tooltip
    document.getElementById("title").setAttribute("title", "This book already exists.");
    //Initalize the tooltip
    $('#title').tooltip();
  }
  //If the value of the grade dropdown is empty...
   else if (document.getElementById("grade").value === ""){
     //Highlight the box in red
    document.getElementById("grade").setAttribute("class", "custom-select border border-danger");
    //Set the contents of the tooltip
    document.getElementById("grade").setAttribute("title", "Please Select an Item");
    //Initalize the tooltip
    $('#grade').tooltip();
  }

  //Same thing, but if the value is null
   else if (document.getElementById("grade").value === null){
     //Highlight the box in red
    document.getElementById("grade").setAttribute("class", "custom-select border border-danger");
    //Set the contents of the tooltip
    document.getElementById("grade").setAttribute("title", "Please Select an Item");
    //Initalize the tooltip
    $('#grade').tooltip();
 }
 //If the value of the title box is empty...
  else if (document.getElementById("title").value === ""){
    //Highlight the box in red
   document.getElementById("title").setAttribute("class", "custom-select border border-danger");
   //Set the contents of the tooltip
   document.getElementById("title").setAttribute("title", "Please enter a title");
   //Initalize the tooltip
   $('#title').tooltip();
 }

 //If the value of the title box is empty...
  else if (document.getElementById("title").value === null){
    //Highlight the box in red
   document.getElementById("title").setAttribute("class", "custom-select border border-danger");
   //Set the contents of the tooltip
   document.getElementById("title").setAttribute("title", "Please enter a title");
   //Initalize the tooltip
   $('#title').tooltip();
 }

   //If all checks are met...
   else {
    //Get the form
    var frm = document.getElementById('newbook');
    frm.submit(); // Submit the form
    frm.reset();  // Reset all form data
   }

}
