(function () {
    /*
        We use an IIFE to properly encapsulate all JavaScript code and prevent
        leaking anything into global scope.
     */
    var choicesSelectionWrapper = jQuery('.otdm__choices-selection');
    var choicesTable = jQuery('.otdm__choices-table');
    var waitingText = jQuery('.otdm__waiting');

    var confirmationButtonWrapper = jQuery('.otdm__confirm-button-wrapper');
    var confirmationButton = jQuery('.otdm__confirm-button');
    var confirmationWrapper = jQuery('.otdm__player-confirmation');
    var confirmationNo = jQuery('.otdm__confirmation-no');

    var result = jQuery('input.otdm__value');

    /* === === === === === ===
        Radio Handling
     * === === === === === === */

    getAllRadios().on('click', function () {
        var input = jQuery(this);
        var selected = getRadioInfo(input);
        result.val(selected.index);
        updateConfirmationText(input);
        confirmationButtonWrapper.show();
        waitingText.hide();

        getAllRadios().each(function () {
            var radio = jQuery(this);
            var info = getRadioInfo(radio);
            var isSelected = isInSelectedGroup(selected, info);
            if (isSelected !== undefined) {
                if (isSelected) {
                    radio.prop('checked', true);
                } else {
                    radio.prop('checked', false);
                }
            }
        });
    });

    var clearHover;
    getAllLabels().hover(function () {
        if (clearHover) {
            clearTimeout(clearHover);
        }

        var label = jQuery(this);
        var input = label.find('> .otdm__choice-input');
        var selected = getRadioInfo(input);
        label.closest('td').addClass('highlight');

        getAllRadios().each(function () {
            var radio = jQuery(this);
            var info = getRadioInfo(radio);
            var isSelected = isInSelectedGroup(selected, info);
            if (isSelected !== undefined) {
                if (isSelected) {
                    radio.closest('td').addClass('highlight');
                } else {
                    radio.closest('td').removeClass('highlight');
                }
            }
        });
    }, function () {
        clearHover = setTimeout(function () {
            getAllLabels().each(function () {
                jQuery(this).closest('td').removeClass('highlight');
            });
        }, 200);
    });

    /* === === === === === ===
        Confirmation Handling
     * === === === === === === */

    confirmationButton.on('click', function () {
        choicesSelectionWrapper.hide();
        confirmationButtonWrapper.hide();
        confirmationWrapper.show();
    });

    confirmationNo.on('click', function () {
        choicesSelectionWrapper.show();
        confirmationButtonWrapper.show();
        confirmationWrapper.hide();
    });

    function updateConfirmationText(selectedRadio) {
        var row = selectedRadio.closest('tr');
        var info = getRadioInfo(selectedRadio);
        var tbody = row.closest('tbody').first();
        var rowIndex = tbody.children('tr').index(row);
        if (rowIndex + 1 < tbody.children('tr').length) {
            row = tbody.children('tr').eq(rowIndex + 1);
        }

        var leftContent = row.find('td:first-child').html();
        var rightContent = row.find('td:last-child').html();
        confirmationWrapper.find('.otdm__confirmation-either')
            .html(info.value === 'A' ? rightContent : leftContent);
        confirmationWrapper.find('.otdm__confirmation-other')
            .html(info.value === 'A' ? leftContent : rightContent);
    }

    /* === === === === === ===
        Utility Functions
     * === === === === === === */

    function getAllRadios() {
        return choicesTable.find('.otdm__choice-input');
    }

    function getAllLabels() {
        return choicesTable.find('.otdm__choice-cell > label');
    }

    /**
     * Returns an object with the name of the radio button (`otdm__option_weekN`),
     * the entry index (1-based), the value (`A` or `B`), and the week of the choice.
     *
     * @param {jQuery} radio
     * @return {{index: number, name: string, value: string, week: number}}
     */
    function getRadioInfo(radio) {
        var index = parseInt(radio.data('index'));
        var name = radio.attr('name');
        var value = radio.val();
        var week = parseInt(radio.data('week'));
        return {
            index: index,
            name: name,
            value: value,
            week: week,
        };
    }

    function isInSelectedGroup(selected, check) {
        if (check.name === selected.name) {
            if (check.value !== selected.value) {
                return false;
            }
            return undefined;
        }

        if (check.value === selected.value) {
            return check.index < selected.index;
        } else {
            return check.index >= selected.index;
        }
    }
}());
