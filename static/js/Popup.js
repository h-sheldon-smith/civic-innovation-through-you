(function () {
    function ready(fn) {
        if (document.readyState !== "loading") fn();
        else document.addEventListener("DOMContentLoaded", fn);
    }

    ready(() => {
        //Collect all open and close modal buttons
        const openButtons = document.querySelectorAll('[data-modal-target]')
        const closeXButtons = document.querySelectorAll('[data-close-x-button]')
        const closeButtons = document.querySelectorAll('[data-close-button]')

        //Make event listeners for all the buttons
        openButtons.forEach(button => {
            button.addEventListener('click', () => {
                const modal = document.querySelector(button.dataset.modalTarget); //uses modal id
                openModal(modal);
            })
        })

        closeXButtons.forEach(button => {
            button.addEventListener('click', () => {
                const modal = button.closest('.modal-backdrop') //finds the closest modal wrapper with this class
                closeModal(modal);
            })
        })

        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                const modal = button.closest('.modal-backdrop') //finds the closest modal wrapper with this class
                closeModal(modal);
            })
        })

        //Open and Close functions for the modals
        function openModal(modal) {
            modal.classList.add("is-open");
            modal.setAttribute("aria-hidden", "false");

            if(modal.id === "submit-idea-modal"){
                listenForSubmitForm(modal);
            }

            // Click outside the modal closes it
            modal.addEventListener("click", (e) => {
                if (e.target === modal) closeModal(modal);
            });

            // Click ESC key closes it
            document.addEventListener("keydown", (e) => {
                if (e.key === "Escape") closeModal(modal);
            });
        }

        function closeModal(modal) {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");

            //If the modal contains the resident idea form, clear it
            if(modal.id === "submit-idea-modal"){
                const idea_form = modal.querySelector('#idea_form');
                idea_form.reset();
            }
        }




        function listenForSubmitForm(modal){
            const idea_form = modal.querySelector('#idea_form');
            const not_submitted_header = modal.querySelector("#not-submitted-title");
            const submitted_header = modal.querySelector("#submitted-title");
            const message = modal.querySelector("#thanks-message");
            const xclosebttn = modal.querySelector("#close-x-idea-modal");
            const closebttn = modal.querySelector("#close-idea-modal");

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
        }
  });
})();