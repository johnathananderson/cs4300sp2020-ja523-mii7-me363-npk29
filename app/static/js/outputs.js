$(document).ready(function () {
    console.log(array);

    $(".filter-button").click(function () {
        var value = $(this).attr('data-filter');

        if (value == "Alphabetical") {
            //$('.filter').removeClass('hidden');
            $('.filter').show('1000');
            console.log(alphabetical);
        } else {
            //            $('.filter[filter-item="'+value+'"]').removeClass('hidden');
            //            $(".filter").not('.filter[filter-item="'+value+'"]').addClass('hidden');
            $(".filter").not('.' + value).hide('3000');
            $('.filter').filter('.' + value).show('3000');

        }
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

});