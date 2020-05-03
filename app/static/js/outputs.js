$(document).ready(function () {
    console.log(array);
    console.log(alphabetical);
    console.log(healthiest);
    $('.filter').not('.default').hide();

    $(".filter-button").click(function () {
        var value = $(this).attr('data-filter');
        $('.filter').filter('.' + value).show('2000');
        $('.filter').not('.' + value).hide('2000')
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

});