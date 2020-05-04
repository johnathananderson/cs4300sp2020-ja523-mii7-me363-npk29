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

    $("#brand-input").bind("input", function () {
        var value = $(this).val();
        console.log("filter")
        console.log(value);
        console.log(filter);
        $('.' + filter + ":hidden").filter(':contains(' + value + ')').show('3000');
        $('.' + filter + ":visible").filter(':not(:contains(' + value + '))').hide('3000');
    });

});