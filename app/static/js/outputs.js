$(document).ready(function () {
    $('.filter:visible').not('.default').hide();
    var filter = "default";

    $(".filter-button").click(function () {
        filter = $(this).attr('data-filter');
        $('.' + filter).show('3000');
        $('.filter:visible').not('.' + filter).hide('3000');
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

    $("#brand-input").input(function () {
        var value = $(this).attr('value');
        $('.' + filter + ":hidden").filter(':contains(' + value + ')').show('3000');
        $('.' + filter + ":visible").filter(':not(:contains(' + value + '))').hide('3000');
    });

});