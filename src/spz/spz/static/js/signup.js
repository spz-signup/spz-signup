function check_and_change_kit_visibilty() {
    'use strict';

    // XXX: read this from our server data
    if ($('#origin').find('option:selected:contains(\'Fakultät\')').length > 0) {
        $('.kit-only').slideDown();
    } else {
        $('.kit-only').slideUp();
    }
}

function show_mail_suggestion(html) {
    var helpBlock = $('#mail').closest('.field').find('.help-block');
    helpBlock.html(html);
    helpBlock.find('#suggestion').click(function() {
        $('#mail').val($(this).text());
        helpBlock.empty();
    });
}

$(document).ready(function() {
    'use strict';

    $('.ui.form').form({
        fields: {
            first_name: {
                identifier: 'first_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Bitte geben Sie einen Vornamen ein.'
                    }
                ]
            },
            last_name: {
                identifier: 'last_name',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Bitte geben Sie einen Nachnamen ein.'
                    }
                ]
            },
            phone: {
                identifier: 'phone',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Bitte geben Sie eine Telefonnumer ein.'
                    }
                ]
            },
            mail: {
                identifier: 'mail',
                rules: [
                    {
                        type: 'email',
                        prompt: 'Bitte geben Sie eine gültige E-Mail Adresse ein.'
                    }
                ]
            },
            origin: {
                identifier: 'origin',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Bitte geben Sie Ihren Bewerberkreis an.'
                    }
                ]
            },
            semester: {
                identifier: 'semester',
                optional: true,
                rules: [
                    {
                        type: 'integer[1..26]',
                        prompt: 'Anzahl der Fachsemester muss zwischen 1 und 26 liegen.'
                    }
                ]
            },
            course: {
                identifier: 'course',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Bitte wählen Sie einen Kurs.'
                    }
                ]
            },
        },
        on: 'blur',
        inline: true,
        transition: 'slide down'
    });

    check_and_change_kit_visibilty();

    // do it again when garlic did its job
    $('#origin').garlic({
        onRetrieve: function() {
            check_and_change_kit_visibilty();
        }
    });

    $('#origin').change(function() {
        check_and_change_kit_visibilty();
    });

    $('#mail').on('blur', function() {
        $(this).mailcheck({
            domains: mailcheckDomains['domains'],
            topLevelDomains: mailcheckDomains['topLevelDomains'],

            suggested: function(element, suggestion) {
                show_mail_suggestion('Meinten Sie <em><a id="suggestion" href="#mail">' + suggestion['full'] + '</a></em>?');
            },

            empty: function() {
                $('#mail').closest('.field').find('.help-block').empty();
            }
        });

        // Check if KIT email
        if ($(this).val().endsWith('@kit.edu')) {
            var studentEmail = $(this).val().replace('@kit.edu', '@student.kit.edu');
            show_mail_suggestion('Studentische KIT E-Mail-Adressen enden auf "@student.kit.edu". Möchtest du <em><a id="suggestion" href="#mail">' + studentEmail + '</a></em> verwenden?');
        }
    });

});
