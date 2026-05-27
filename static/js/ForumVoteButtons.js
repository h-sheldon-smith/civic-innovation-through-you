(function() {
    if (window.ForumVoteInitialized) {
        return;
    }

    window.ForumVoteInitialized = true;

    document.addEventListener('DOMContentLoaded', function() {
        const postsContainer = document.getElementById('thread-posts-container');

        // If the thread's posts container isn't on this page, return
        if (!postsContainer) {
            return;
        }

        // Attach one event listener to the posts' parent container
        postsContainer.addEventListener('click', function(event) {
            const voteButton = event.target.closest('.vote-btn');

            // If the click wasn't on a vote button, return
            if (!voteButton) {
                return;
            }

            // Prevent default behavior (e.g., if it's inside a form)
            event.preventDefault();

            // Extract the clicked button's data from its data attributes
            const postId = voteButton.getAttribute('data-post-id');
            const voteUrl = voteButton.getAttribute('data-vote-url');
            const likedText = voteButton.getAttribute('data-liked-text');
            const notLikedText = voteButton.getAttribute('data-not-liked-text');

            // Get the clicked button's corresponding score <span>
            const scoreSpan = document.getElementById(`score-${postId}`);
            const buttonTextSpan = document.getElementById(`vote-button-text-${postId}`);

            // Disable button temporarily to prevent multi-clicks messing with button update logic
            voteButton.disabled = true;

            // Execute the AJAX request
            fetch(voteUrl, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                return response.json();
            })
            .then(data => {
                // Data is the dict (turned into json) returned by the toggle_post_upvote view

                // Update the DOM for this specific post using the returned vote count
                if (scoreSpan && data.post_score !== undefined) {
                    scoreSpan.textContent = data.post_score;
                }
                
                // Toggle visual classes for it the user upvoted or not in the frontend
                if (data.user_upvoted) {
                    voteButton.classList.add('active');

                    if (buttonTextSpan) {
                        buttonTextSpan.textContent = likedText;
                    }
                } else {
                    voteButton.classList.remove('active');

                    if (buttonTextSpan) {
                        buttonTextSpan.textContent = notLikedText;
                    }
                }
            })
            .catch(error => {
                console.error('Voting failed:', error);
            })
            .finally(() => {
                // Re-enable the button after the request finishes
                voteButton.disabled = false;
            });
        });
    });
})();

// Helper function to extract Django's CSRF cookie
function getCsrfToken() {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }

    return cookieValue;
}