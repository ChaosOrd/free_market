var navigation = {
    Init: function()
    {
        $('input').keypress(function(e) {
            navigation.FocusOnNextTabindexIfNeeded(e);
        });


        $('select').keypress(function(e) {
            navigation.FocusOnNextTabindexIfNeeded(e);
        });
    },
    IsSubmit: function(element)
    {
        if (element.type == "submit")
        {
            return true;
        }

        return false;
    },

    FocusOnNextTabindexIfNeeded: function(e)
    {
        if (e.which == 13 && navigation.IsSubmit(e.target) == false)
        {
            var selectedTabIndex = e.currentTarget.tabIndex;
            var elements_with_tabindex = $('[tabindex]');

            var nextTabIndex = Number.MAX_VALUE;
            var nextTabElement = null;
            elements_with_tabindex.each(function(index)
            {
                element = elements_with_tabindex[index];
                if (element.tabIndex > selectedTabIndex && element.tabIndex < nextTabIndex)
                {
                    nextTabIndex = element.tabIndex;
                    nextTabElement = element;
                }
            });

            if (nextTabElement != null)
            {
                nextTabElement.focus();
                e.preventDefault();
            }
        }
    }
};

$(document).ready(function() {
    navigation.Init();
    $('[tabindex=0]').focus();
})
