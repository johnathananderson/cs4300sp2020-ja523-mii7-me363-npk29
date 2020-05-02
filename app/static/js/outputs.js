$(document).ready(function () {
    console.log(array);
    console.log(alphabetical);
    console.log(healthiest);
    $('.filter').not('.default').hide();

    $(".filter-button").click(function () {
        var value = $(this).attr('data-filter');
        $('.filter').filter('.' + value).show('4000');
        $('.filter').not('.' + value).hide('4000')
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

});