$(document).ready(function(){
    'use strict';

    $('.ui.dropdown').dropdown({
        fullTextSearch: true,
        message: {
            noResults: 'Keine Einträge vorhanden.'
        }
    });

    $('.ui.slider').each(function() {
        var t = $(this);
        t.slider({
            min: parseInt(t.attr('data-min')),
            max: parseInt(t.attr('data-max')),
            step:  parseInt(t.attr('data-step')),
            start:  parseInt(t.attr('data-start')),
            onChange: function(value) {
                t.find('input').val(value);
            }
        });
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

    var update = function(input) {
        input.setAttribute('value', input.value);
        input.oldvalue = input.value;
        var labels = $('label[for=' +  input.id + ']');
        labels.hide();
        labels.filter('[for_value=' +  input.value + ']').show();
    }

    $('.ui.tristate input').each(function() {
        this.valueChangedBySliding = false;
        this.slideDirection = 1;
        update(this);
    });

    $('.ui.tristate input').on('input', function() {
        this.valueChangedBySliding = true;
        if (this.value != this.oldvalue) {
            this.slideDirection = this.value - this.oldvalue;
        }
        update(this);
    });

    $('.ui.tristate input').on('click', function(ev) {
        if (!this.valueChangedBySliding) {
            var currentValue = parseInt(this.value);
            if (currentValue <= this.min) this.slideDirection = 1;
            else if (currentValue >= this.max) this.slideDirection = -1;
            var newValue = currentValue + this.slideDirection;
            this.value = newValue;
            update(this);
        }
        this.valueChangedBySliding = false;
    });
});

// contributors welcome :)
console.log('It seems like you are interested in how this project works.\nFeel free to check it out at: https://github.com/spz-signup/spz-signup\nIssues and/or Pull Request welcome! :)');
