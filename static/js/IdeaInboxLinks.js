//inbox page listener
document.addEventListener("DOMContentLoaded", function(){
    const rows = document.querySelectorAll("tr[data-href]");

    async function goToIdea(idea){
        const url = idea.dataset.href;
        window.location = url;
    }

    //listeners for each row
    rows.forEach(row => {
        row.addEventListener("click", () => goToIdea(row));
    })
})
