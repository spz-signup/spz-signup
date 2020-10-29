$(document).ready(function(){
    'use strict';

    $('.ui.dropdown').dropdown({
        fullTextSearch: true,
        message: {
            noResults: 'Keine Einträge vorhanden.'
        }
    });
    window.setTimeout(function(){
        $('.ui.selection.dropdown .menu').css('width', 'calc(100% + 2px)');
    }, 200);

    $('.message .close').on('click', function() {
        $(this).closest('.message').transition('fade');
    });

    $('.ui.checkbox').checkbox();

    moment.locale('de');
    $('.fmt-datetime').each(function (idx, elem) {
        var $elem = $(elem);
        var data = $elem.text();
        var fmt = moment.utc(data).local().format('Do MMMM YYYY, HH:mm');
        if (data === '0001-01-01 00:00:00') {
            fmt = '-∞';
        } else if (data === '9999-12-31 23:59:59.999999') {
            fmt = '+∞';
        }
        $elem.text(fmt);
    });

    $('button[type=reset]').on('click', function() {
        var form = $(this).closest('form');

        // that somehow seems required to really clear all fields
        window.setTimeout(function(){
            $('input[type=radio]', form).removeAttr('checked');
            $('input[type=text]', form).val('');
            $('.ui.dropdown', form).dropdown('clear');
            $('input', form).garlic('destroy');
        }, 10);
    });

    $('.skip_label').on('change', function() {
        var input = $(this).find('input')
        var checked = input.is(':checked');
        var mainInput = $('#' + input.attr('name').replace('_skipped', ''));
        mainInput.attr('readonly', checked);
        if (checked) {
            mainInput.val(input.data('value').trim());
        } else {
            mainInput.val('');
        }
    });
});

// contributors welcome :)
console.log('It seems like you are interested in how this project works.\nFeel free to check it out at: https://github.com/spz-signup/spz-signup\nIssues and/or Pull Request welcome! :)');
