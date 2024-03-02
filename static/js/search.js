jQuery(document).ready(function($) {
    $("#pigeonSearch").on("keyup", function(event) {
        location.href="?name=" + $(this).val() + "&currentSearch=" + $(this).val();
    });

    $("#pigeonSearchButton").on("click", function(event) {
        location.href="?name=" + $("#pigeonSearch").val();
    });
});