const imageInput = document.getElementById('donate_image');
const titleInput = document.getElementById('donate_title');
const descriptionInput = document.getElementById('donate_description');
const locationInput = document.getElementById('donate_location');
const categoryInput = document.getElementById('donate_category');
const imageDescription = document.getElementById('donate_image_description');
const resetButton = document.getElementById('donate_reset');
const donationForm = document.getElementById('donation_form');

function validateImage() {
    const file = imageInput.files[0];
    if(!file)
        return true;
    const fsize = file.size / 1024;
    imageDescription.innerHTML = "Image size: " + fsize.toFixed(2) + "KB.";
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

function removeClasses(element){
    element.classList.remove('is-valid');
    element.classList.remove('is-invalid');
}

function validateForm(){
    const title = titleInput.value;
    const description = descriptionInput.value;
    const location = locationInput.value;
    const category = categoryInput.value;

    var formOk = true;


    if(title.length == 0) {
        makeInvalid(titleInput);
        formOk = false;
    }
    else
        makeValid(titleInput);


    if(description.length < 15){
        makeInvalid(descriptionInput);
        formOk = false;
    }
    else
        makeValid(descriptionInput);


    if(location.length == 0){
        formOk = false;
        makeInvalid(locationInput);
    }
    else
        makeValid(locationInput);


    if(category.length == 0){
        formOk = false;
        makeInvalid(categoryInput);
    }
    else
        makeValid(categoryInput);


    if(!validateImage()){
        makeInvalid(imageInput);
        formOk = false;
    }
    else
        makeValid(imageInput);
    return formOk;
}

titleInput.onchange = function () {
    const title = titleInput.value;
    if(title.length > 0)
        makeValid(titleInput);
    else
        makeInvalid(titleInput);
}

descriptionInput.onchange = function () {
    const description = descriptionInput.value;
    if(description.length >= 15)
        makeValid(descriptionInput);
    else
        makeInvalid(descriptionInput);
}

imageInput.onchange = function (){
    donationForm.classList.remove('was-validated');
    if(!validateImage()) {
        imageInput.classList.remove('is-valid');
        imageInput.classList.add('is-invalid');
    }
    else {
        imageInput.classList.remove('is-invalid');
        imageInput.classList.add('is-valid');
    }
};

resetButton.onclick = function () {
    donationForm.classList.remove('was-validated');
    removeClasses(titleInput);
    removeClasses(descriptionInput);
    removeClasses(locationInput);
    removeClasses(categoryInput);
    removeClasses(imageInput);
}

