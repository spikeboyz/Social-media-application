document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            
            fetch(`/delete_comment/${commentId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Post deleted');
                    location.reload();
                } else {
                    console.error('Failed to delete comment');
                }
            })
            .catch(error => {
                
                console.error('Error:', error);
            });
        });
    });
});