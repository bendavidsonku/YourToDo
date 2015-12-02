$(document).ready(function() {

   loadUserAccountInformation(false);
});

function loadUserAccountInformation(appendSuccess) {

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
            if (appendSuccess == false)
            {
                $('#user-account-information-render-area').empty().append(data);  
            }
            else
            {
                $('#user-account-information-render-area').empty().append(data);
                $('#update-profile-success-message-render-area').empty().append("Profile Updated Succesfully");
                $('#update-profile-success-message-render-area').show();
            }
            
        },
    });
}