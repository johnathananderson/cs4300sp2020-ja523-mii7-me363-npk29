$(document).ready(function () {
    console.log(array);
    console.log(alphabetical);
    console.log(healthiest);
    $('.filter').not('.default').hide();

    $(".filter-button").click(function () {
        var value = $(this).attr('data-filter');
        $('.filter').filter('.' + value).show('3000');
        $('.filter').not('.' + value).hide('3000')
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

});