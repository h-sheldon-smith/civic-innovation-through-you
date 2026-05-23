document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.vote-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const postId = this.dataset.postId;
            const voteUrl = this.dataset.voteUrl;
            const scoreElement = document.getElementById(`score-${postId}`);
            
            // Retrieve Django's standard CSRF token cookie value
            const csrftoken = document.cookie.split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1];

            fetch(voteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update the numerical score tracking element text
                scoreElement.textContent = data.score;
                
                // Toggle visual button highlight states based on return statuses
                if (data.voted) {
                    this.classList.add('voted');
                } else {
                    this.classList.remove('voted');
                }
            })
            .catch(error => console.error('Error processing vote interaction:', error));
        });
    });
});