$(document).ready(function () {
    $('.filter:visible').not('.default').hide();

    $(".filter-button").click(function () {
        var value = $(this).attr('data-filter');
        $('.filter:hidden').filter('.' + value).show('3000');
        $('.filter:visible').not('.' + value).hide('3000')
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

});