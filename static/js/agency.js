// Agency Theme JavaScript
$( document ).ready(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 100)
        }, 1250, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar',
        offset: 0
    });

    var windowWidth = $(window).width();
    if(windowWidth < 768){
        $('a.page-scroll').bind('click', function(event) {
            var $anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: ($($anchor.attr('href')).offset().top - 65)
            }, 1000, 'easeInOutExpo');
            event.preventDefault();
        });
    }

    // Closes the Responsive Menu on Menu Item Click
    $('.menu.navbar-collapse a').click(function(){
            $('.menu.navbar-toggle:visible').click();
    });

    // Closes the Responsive Service on Menu Item Click
    $('.service-menu ul li a').click(function(){
            $('.service.navbar-toggle:visible').click();
    });


    $('.menu-service').on('show.bs.collapse', function () {
        var actives = $(this).find('.collapse.in'),
            hasData;

        if (actives && actives.length) {
            hasData = actives.data('collapse')
            if (hasData && hasData.transitioning) return
            actives.collapse('hide')
            hasData || actives.data('collapse', null)
        }
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 57
        }
    })

    $('.service-menu').affix({
        offset: {
            top: 57
        }
    })


    //login-box-pop-up
    $('a.login-window').click(function() {
        //Getting the variable's value from a link
        var loginBox = $(this).attr('href');

        //Fade in the Popup
        $(loginBox).fadeIn(300);

        //Set the center alignment padding + border see css style
        var popMargTop = ($(loginBox).height() + 24) / 2;
        var popMargLeft = ($(loginBox).width() + 24) / 2;

        $(loginBox).css({
            'margin-top' : -popMargTop,
            'margin-left' : -popMargLeft
        });

        // Add the mask to body
        $('body').append('<div id="mask"></div>');
        $('#mask').fadeIn(300);

        return false;
    });

    // When clicking on the button close or the mask layer the popup closed
    $('a.close, #mask').on('click', function() {
        $('#mask ,.login-popup').fadeOut(300 , function() {
        $('#mask').remove();
        });
        return false;
    });

    $(document).keyup(function(e) {

    if (e.keyCode == 27) { $('#mask ,.login-popup').fadeOut(300 , function() {
    $('#mask').remove();
    });
    return false; }   // esc
    });

    // Dynamically Add and Remove full Form
    $(function () {
        $("#addButton").on("click", function () {
            var counter = $(".type").length;

            if (counter > 10) {
                alert("Only 5 textboxes allow");

                return false;
            }

            var newType = $(".type").first().clone().addClass("newAdded");
            var newName = $(".name").first().clone().addClass("newAdded");

            newType.appendTo("#TextBoxesGroup");
            newName.appendTo("#TextBoxesGroup");
        });

        $("#removeButton").click(function () {
            var counter = $(".type").length;

            if (counter == 1) {
                alert("No more textbox to remove");

                return false;
            }

            $(".type").last().remove();
            $(".name").last().remove();
        });

        $("#resetButton").click(function () {
            $(".newAdded").remove();
        });
    });

    // Dynamically Add and Remove width-height-unite
    $('.multi-field-wrapper').each(function() {
        var $wrapper = $('.multi-fields', this);
        $(".add-field", $(this)).click(function(e) {
            $('.multi-field:first-child', $wrapper).clone(true).appendTo($wrapper).find('input').val('').focus();
        });
        $('.multi-field .remove-field', $wrapper).click(function() {
            if ($('.multi-field', $wrapper).length > 1)
                $(this).parent('.multi-field').remove();
        });
    });


    //Attachments
    $('#our-test').MultiFile({
        STRING: {
            remove: '<i class="fa fa-times" aria-hidden="true"></i>',
            denied: 'You cannot select a $ext file.\nTry again...',
            file: '$file',
            selected: 'File selected: $file',
            duplicate: 'This file has already been selected:\n$file',
            toomuch: 'The files selected exceed the maximum size permited ($size)',
            toomany: 'Too many files selected (max: $max)',
            toobig: '$file is too big (max $size)'
        },
        onFileChange: function(){
            console.log(this, arguments);
        }
    });

     $(".owl-carousel").owlCarousel({
        items: 1,
        singleItem: true,
        navigation: true,
        navigationText: ["",""],
        pagination: true,
        scrollPerPage: true,
        autoPlay: true,
        paginationNumbers:true,
     });


    //Back To Top
    $("#back-to-top").hide();
    $(window).scroll(function(){
        if ($(window).scrollTop()>100){
            $("#back-to-top").fadeIn(300);
        }
        else
        {
            $("#back-to-top").fadeOut(300);
        }
    });
    $("#back-to-top").click(function(){
        $('body,html').animate({scrollTop:0},1000);
        return false;
    });
});
