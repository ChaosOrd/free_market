
var CustomPopulation = {
    Init: function() {
        this.subscribeToItemRemovers();
    },

    addToSupplyDemand: function (data) {
        $('#supplies_demands').append(data);
        var nextSdNum = $('#next_sd_num');
        nextSdNum.val(parseInt(nextSdNum.val()) + 1);
        navigation.Init();
        CustomPopulation.Init();
    },

    subscribeToItemRemovers: function() {
        var itemRemovers = $("a[remove_target]");
        var numOfItemsToRemove = itemRemovers.length;

        itemRemovers.click( function(e) {
            var itemRemover = e.target;
            var itemToRemoveId = itemRemover.attributes["remove_target"].value;
            $('#' + itemToRemoveId).remove();
        });
    }
};

$(document).ready(function() {
    CustomPopulation.Init();
    $('[tabindex=0]').focus();
    $("#add_supply_demand").click( function () {
        $.ajax({
            url: '/population/supply_demand_form/' +  $('#next_sd_num').val(),
            type: 'get',
            success: CustomPopulation.addToSupplyDemand
        });
    });
})
