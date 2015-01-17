var navigation = {
    IsTextBox: function (element)
    {
        if (element.is('input') && element.prop('type') == "text")
        {
            return true;
        }

        return false;
    }
};

$(document).ready(function() {
    $('[tabindex=0]').focus();
})

$('input').keypress(function(e) {
    if (e.which == 13)
    {
        var selected_tab_idx = e.currentTarget.tabIndex;
        $('[tabindex=' + (selected_tab_idx + 1) + ']').focus();
        e.preventDefault();
    }
});
