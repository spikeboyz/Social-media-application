document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            
            fetch(`/delete_post/${postId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Post deleted');
                    location.reload();
                } else {
                    console.error('Failed to delete post');
                }
            })
            .catch(error => {
                
                console.error('Error:', error);
            });
        });
    });
});


  