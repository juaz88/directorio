jQuery(document).ready(function($) {

    // Smooth scroll for the menu and links with .scrollto classes
    $('.smoothscroll').on('click', function(e) {
        e.preventDefault();
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            if (target.length) {

                $('html, body').animate({
                    scrollTop: target.offset().top - 48
                }, 1500, 'easeInOutExpo');
            }
        }
    });

    $(".navbar-collapse a").on('click', function() {
        $(".navbar-collapse.collapse").removeClass('in');
    });
});


$('.btn').click(function() {
    $(this).toggleClass("click");
    $('.sidebar').toggleClass("show");
});


$('.sidebar ul li a').click(function() {
    var id = $(this).attr('id');
    $('nav ul li ul.item-show-' + id).toggleClass("show");
    $('nav ul li #' + id + ' span').toggleClass("rotate");

});

$('nav ul li').click(function() {
    $(this).addClass("active").siblings().removeClass("active");
});