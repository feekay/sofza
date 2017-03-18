$( document ).ready(function() {
    // get id from url
    var url = window.location.href;
    var id = url.substring(url.lastIndexOf('#') + 1);

    // find current page through href attr
    $(".navbar-nav li a").each(function(){
        var bob = $(this).attr('href');
        if(bob === "#"+id)
        {
            $(".navbar-nav li").removeClass('active')
            $(this).parent().addClass('active')
        }
    });

    // onclick active class
    $(".navbar-nav li a").click(function(){
        $('.navbar-nav li').removeClass('active');
        $(this).parent().addClass('active');
    });

    $("#"+id).css("padding-top", "140px");
    //alert(id);

    $(window).bind('mousewheel', function(e) {
        if(e.originalEvent.wheelDelta / 120 > 0) {
            $("#"+id).css("padding-top", "40px");
        } else {
            $("#"+id).css("padding-top", "40px");
        }
    });

    $(".homepage .navbar-nav li a").click(function(){
        $('.navbar-nav li').removeClass('active');
        $("#"+id).css("padding-top", "40px");
    });

});