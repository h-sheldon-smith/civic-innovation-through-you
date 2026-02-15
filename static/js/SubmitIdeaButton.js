document.addEventListener("DOMContentLoaded", function(){
    const idea_form = document.getElementById("idea_form");
    const message = document.getElementById("thanks-message");
    const xclosebttn = document.getElementById("close-modal");
    const closebttn = document.getElementById("close-modal-2");
    const submitted_header = document.getElementById("submitted-title");
    const not_submitted_header = document.getElementById("not-submitted-title");

    if(!idea_form){
        console.log("The idea form was not successfully found");
        return;
    }

    idea_form.addEventListener("submit", async function (event){
        event.preventDefault(); //stop automatic submit behavior which will cause the page to reload
        const formData = new FormData(idea_form); //gather user input, csrf token
        const url = idea_form.action;

        //send data, get response WITHOUT reloading the popup
        const response = await fetch(url, {
            method: "POST",
            body: formData
        });

        const reply = await response.json();

        //If successful, hide the form and show the success message
        if (reply.success){
            submitted_header.style.display = "inline";
            not_submitted_header.style.display = "none";
            idea_form.style.display = "none";
            message.style.display = "inline";
            xclosebttn.style.display = "none";
            closebttn.style.display = "inline";
        //If failure, show a popup message
        } else {
            alert("We did not receive your ideas. Please check all fields or retry later");
        }

    })
})