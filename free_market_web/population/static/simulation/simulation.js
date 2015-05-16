$(document).ready(function() {
    $.agax({
        url: '/population/simulation_result/' + $('#simulated_universe_id').val(),
        type: 'get',
        success: function(data) {
            var sim_result = data;
        };
});
