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


$(document).ready(function () {
    $('input[tabindex=0]').focus();
    document.onkeypress=function(e) {
        e = e || window.event;
        var selected_tab_idx = document.activeElement.tabIndex;
        if (e.which == 13 && navigation.IsTextBox($(document.activeElement)))
        {
            $('input[tabindex=' + (selected_tab_idx + 1) + ']').focus();
        }
    }
});

