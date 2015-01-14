var Navigation = {
    function IsTextbox(element)
    {
        if (element.tagName && element.tagName.toLowerCase() == "input" && textbox.type.toLowerCase() == "textbox")
        {
            return true;
        }

        return false;
    }
}

$(document).ready(function () {
    document.onkeypress=function(e) {
        e = e || window.event;
        var selected_tab_idx = document.activeElement.tabIndex;
        if (e.which == 13 )
        {
            $('input[tabindex=' + (selected_tab_idx + 1) + ']').focus();
        }
    }
});
