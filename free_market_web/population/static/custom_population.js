
$(document).ready(function() {
    $("#add_demand").click( function () {
        $("#demands").append($("#prototypes #demand").clone());
    })

    $("#add_supply").click( function () {
        $("#supplies").append($("#prototypes #supply").clone());
    })
})
