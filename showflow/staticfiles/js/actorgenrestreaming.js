$(document).ready(function() {
    $("#actorCreate").click(function() {
        $("#actorCreateForm").toggle();
        $("#actorCreate i").toggleClass("fa-plus fa-minus");
    });

    $("#genreCreate").click(function() {
        $("#genreCreateForm").toggle();
        $("#genreCreate i").toggleClass("fa-plus fa-minus");
    });

    $("#streamingCreate").click(function() {
        $("#streamingCreateForm").toggle();
        $("#streamingCreate i").toggleClass("fa-plus fa-minus");
    });
});