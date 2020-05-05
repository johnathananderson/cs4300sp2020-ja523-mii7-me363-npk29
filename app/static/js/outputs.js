$(document).ready(function () {
    $('.filter:visible').not('.default').hide();
    var filter = "default";
    var value = "";

    $.expr[":"].contains = $.expr.createPseudo(function (arg) {
        return function (elem) {
            return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
        };
    });

    $(".filter-button").click(function () {
        filter = $(this).attr('data-filter');
        $('.' + filter).filter(':contains(' + value + ')').show('3000');
        $('.filter:visible').not('.' + filter).hide('3000');
    });

    if ($(".filter-button").removeClass("active")) {
        $(this).removeClass("active");
    }
    $(this).addClass("active");

    $("#brand-input").bind("input", function () {
        value = $(this).val();
        $('.' + filter + ":hidden").filter(':contains(' + value + ')').show('3000');
        $('.' + filter + ":visible").filter(':not(:contains(' + value + '))').hide('3000');
    });

});