$(document).ready(function() {

   loadUserAccountInformation();
});

function loadUserAccountInformation() {

    var injectUserAccountPage = "ready";

    $.ajax({
        url: "/user-account-information/",
        type: "POST",
        dataType: 'html',
        data:
        {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            load_user_information_form: injectUserAccountPage
        },
        success: function(data, textStatus, jqXHR) {
            $('#user-account-information-render-area').empty().append(data);
        },
    });
}