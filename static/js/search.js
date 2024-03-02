jQuery(document).ready(function($) {
    $("#pigeonSearch").on("keyup", function(event) {
        if (event.keyCode === 13) {
            location.href="?name=" + $(this).val();
        }
    });

    $("#pigeonSearchButton").on("click", function(event) {
        location.href="?name=" + $("#pigeonSearch").val();
    });
});