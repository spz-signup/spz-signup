$(document).ready(function(){
    'use strict';

    $('.ui.accordion').accordion();

    $('.ui.filter.form').change(function(ev){
        $(this).submit()
    });

    $('.ui.filter.form').submit(function(ev){
        var data = new FormData(ev.target);
        var waitinglist = data.get('include_waitinglist');
        var vacancies = data.get('include_vacancies');
        var languages = data.getAll('language_filter');
        applyFilter(waitinglist, vacancies, languages);
        return false;
    });
});

function applyFilter(waitinglist, vacancies, languages) {
    console.log(waitinglist, vacancies, languages);
    $('.ui.language.card').each(function(){
        if (languages.includes($(this).attr('data-language'))) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}
