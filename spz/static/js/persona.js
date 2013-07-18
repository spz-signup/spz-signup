$(function() {
  $('a.signin').on('click', function() {
    navigator.id.request({
      siteName: 'KIT Sprachenzentrum'
    });
    return false;
  });

  $('a.signout').on('click', function() {
    navigator.id.logout();
    return false;
  });

  navigator.id.watch({
    loggedInUser: $CURRENT_USER,
    onlogin: function(assertion) {
      var box = $('<div class="signinprogress"></div>')
        .hide()
        .text('Please wait ...')
        .appendTo('container')
        .fadeIn('fast');
      $.ajax({
        type: 'POST',
        url: $URL_ROOT + '_auth/login',
        data: {assertion: assertion},
        success: function(res, status, xhr) { window.location.reload(); },
        error: function(xhr, status, err) {
          box.remove();
          navigator.id.logout();
          alert('Login failure: ' + err);
        }
      });
    },
    onlogout: function() {
      $.ajax({
        type: 'POST',
        url: $URL_ROOT + '_auth/logout',
        success: function(res, status, xhr) { window.location.reload(); },
        error: function(xhr, status, err) {
          alert('Logout failure: ' + err);
        }
      });
    }
  });
});
