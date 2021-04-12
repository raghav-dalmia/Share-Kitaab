// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  var id_token = googleUser.getAuthResponse().id_token;
  const id = profile.getId();
  const name = profile.getName();
  const image_url = profile.getImageUrl();
  const email = profile.getEmail();

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/signup/google');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    var new_url = xhr.responseText;
    const index_url = "http://localhost:5000/";
    new_url = new_url.substr(1, new_url.length-3);
    window.location.href = index_url + new_url;
  };
  xhr.send(
      'g_signup_id=' + id +
      "&g_signup_name=" + name +
      '&g_signup_image_url=' + image_url +
      '&g_signup_email=' + email
  );
}
