// handles updating the voting buttons' UI without the user needing to refresh the page
document.addEventListener('DOMContentLoaded', () => {
    // Attach listener to all voting buttons
    document.querySelectorAll('.vote-btn').forEach(button => {
      button.addEventListener('click', async (e) => {
        e.preventDefault();
        
        const postId = button.dataset.postId;
        const scoreElement = document.getElementById(`score-${postId}`);
        
        // Target the JSON view we created earlier
        const url = button.dataset.voteUrl; 
        
        try {
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'X-CSRFToken': '{{ csrf_token }}',
              'Content-Type': 'application/json'
            }
          });
          
          if (response.ok) {
            const data = await response.json();
            
            // Update the UI with fresh cached counts from django-vote
            scoreElement.textContent = data.score;
            
            if (data.voted) {
              button.classList.add('voted');
            } else {
              button.classList.remove('voted');
            }
          }
        } catch (error) {
          console.error('Voting failed:', error);
        }
      });
    });
  });