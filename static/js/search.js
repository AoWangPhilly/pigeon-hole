jQuery(document).ready(function($) {
    $("#pigeonSearch").on("keyup", function(event) {
        if(event.key === "Enter") {
            location.href="?name=" + $(this).val() + "&currentSearch=" + $(this).val();
        }
    });

    $("#pigeonSearchButton").on("click", function(event) {
        location.href="?name=" + $("#pigeonSearch").val() + "&currentSearch=" + $("#pigeonSearch").val();
    });
});