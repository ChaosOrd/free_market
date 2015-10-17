$(document).ready(function() {
    $.ajax({
        url: '/population/simulation_result/' + $('#simulated_universe_id').text() + "/",
        type: 'get',
        success: function (data) {
            var sim_result = data;
        }
    });
});
