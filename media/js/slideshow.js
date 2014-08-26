$(function() {
  $(".slideshow img:gt(0)").hide();

  setInterval(function() { 
    $('.slideshow :first-child')
      .fadeOut()
      .next('img')
      .fadeIn()
      .end()
      .appendTo('.slideshow');
  },  10000);
});
