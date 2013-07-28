/**
 * Google Plus sign-in callback
 */
var onSignInCallback = function(authResult) {
    if (authResult.access_token) {
        $('#connected').show()
        $('#signin-button').hide()
        // Pass the auth results back to the server
        $.ajax({
            type: 'POST',
            url: '/login',
            data: authResult.code,
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            success: function(data) {console.log(data)},
            failure: function(errMsg) {console.error('Failed to log in to app')}
        })
    } else {
        $('#connected').hide()
        $('#signin-button').show()
    }
}