$(document).ready(function(){
    'use strict';

    $('.ui.accordion').accordion();

    $('.ui.filter.form').change(function(ev){
        $(this).submit()
    });

    $('.ui.filter.form').submit(function(ev){
        var data = new FormData(ev.target);
        var courseStatus = data.getAll('status_filter');
        var languages = data.getAll('language_filter');
        var gers = data.getAll('ger_filter');
        applyFilter(courseStatus, languages, gers);
        return false;
    });
});

function applyFilter(statusFilter, languages, gers) {
    $('.ui.course.item').each(function(){
        var status = $(this).attr('data-status');
        $(this).toggle(statusFilter.length == 0 || statusFilter.includes(status));
    });
    $('.ui.ger.segment').each(function(){
        var ger = $(this).attr('data-ger');
        $(this).toggle(gers.length == 0 || gers.includes(ger));
    });
    $('.ui.language.card').each(function(){
        var lang = $(this).attr('data-language');
        $(this).toggle(languages.length == 0 || languages.includes(lang));
    });
    $('.ui.ger.segment').not(':has(.ui.course.item:visible)').hide();
    $('.ui.language.card').not(':has(.ui.ger.segment:visible)').hide();
}
