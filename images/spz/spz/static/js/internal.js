$(document).ready(function(){
    'use strict';

    $('.ui.table.sortable').tablesort();

    $('button[data-confirm]').each(function() {
        var msg = $(this).data('confirm');
        $(this).click(function() {
            confirm(msg);
        });
    });
});
