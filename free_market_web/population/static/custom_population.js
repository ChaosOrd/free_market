
var CustomPopulation = {
    addToSupplyDemand: function (data)
    {
        $('#supplies_demands').append(data);
    }
};

$(document).ready(function() {
    $("#add_supply_demand").click( function () {
        $.ajax({
            url: 'supply_demand_form',
            type: 'get',
            success: CustomPopulation.addToSupplyDemand
        });
    })
})
