
var CustomPopulation = {
    addToSupplyDemand: function (data)
    {
        $('#supplies_demands').append(data);
        var nextSdNum = $('#next_sd_num');
        nextSdNum.val(parseInt(nextSdNum.val()) + 1);
        navigation.Init();
    }
};

$(document).ready(function() {
    navigation.Init();
    $('[tabindex=0]').focus();
    $("#add_supply_demand").click( function () {
        $.ajax({
            url: '/population/supply_demand_form/' +  $('#next_sd_num').val(),
            type: 'get',
            success: CustomPopulation.addToSupplyDemand
        });
    })
})
