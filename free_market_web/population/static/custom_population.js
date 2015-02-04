
var CustomPopulation = {
    addToSupply: function (data)
    {
        $('#supplies').append(data);
    },
    addToDemand: function (data)
    {
        $('#demands').append(data);
    }
};

$(document).ready(function() {
    $("#add_demand").click( function () {
        $.ajax({
            url: 'resource_form',
            type: 'get',
            success: CustomPopulation.addToDemand
        });
    })

    $("#add_supply").click( function () {
        $.ajax({
            url: 'resource_form',
            type: 'get',
            success: CustomPopulation.addToSupply
        });
    })
})
