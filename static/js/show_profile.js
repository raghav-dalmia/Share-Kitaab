const deleteModal = document.getElementById('deleteBookModal');
const deleteModalId = document.getElementById('delete_modal_id');
const modalTitle = document.getElementById('deleteModalTitle');
const profilePicInput = document.getElementById('profile_pic_image');
const profilePicDesc = document.getElementById('profile_image_desc');

function sendDeleteRequest() {
    const xhr = new XMLHttpRequest();
    const id = deleteModalId.value;
    const url = "/book/" + id;
    xhr.onload = function () {
        var new_url = xhr.responseText;
        const index_url = "http://127.0.0.1:5000/";
        new_url = new_url.substr(1, new_url.length-3);
        window.location.href = index_url + new_url;
    }
    xhr.open("DELETE", url, true);
    xhr.send(null);
}

deleteModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const id = button.getAttribute('data-bs-whatever')
    const title = button.getAttribute('data-bs-whatever2')

    modalTitle.textContent = "Delete " + title;
    deleteModalId.value = id;
});

function validateImage() {
    const file = profilePicInput.files[0];
    if(!file)
        return true;
    const fsize = file.size / 1024;
    profilePicDesc.innerText = "Please upload a valid image. Image size is: " + fsize.toFixed(2) + " KB.";
    return fsize <= 500;
}

function makeInvalid(element){
    element.classList.remove('is-valid');
    element.classList.add('is-invalid');
}

function makeValid(element){
    element.classList.remove('is-invalid');
    element.classList.add('is-valid');
}

function validateForm(){
    if(validateImage())
        makeValid(profilePicInput);
    else{
        makeInvalid(profilePicInput);
        return false;
    }
    return true;
}

profilePicInput.onchange = function () {
    validateForm();
}