document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('#feed');
    const userDetailsDiv = document.getElementById('user-details');
    const userId = userDetailsDiv.getAttribute('data-user-id');

    function loadPosts() {
        fetch(`/other_profile/${userId}`)
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error('Error retrieving posts');
                }
                return response.json();
            })
            .then(data => {
                console.log("Data acquired");
                console.log(data);
                const userId = data.request_data.user_id;
                console.log(data.posts)
                const parsedPosts = data.posts;
                console.log(parsedPosts)
                parsedPosts.forEach((post, index) => {
                    const timestamp = new Date(post.fields.timestamp);
                    const formattedDate = `${timestamp.toLocaleString('default', { month: 'long' })} ${timestamp.getFullYear()}`;
                    const postDiv = document.createElement('div');
                    console.log(post.picture_link);
                    const isLiked = post.fields.liked_by && post.fields.liked_by.includes(userId);
                    const isFollowing = post.fields.followers.includes(userId); 
                    postDiv.innerHTML = `
                        <h3>${post.fields.name || ''}</h3>
                        <p>Likes: ${post.fields.likes || ''}</p>
                        <img src="${post.fields.picture_link}" alt="Post Image" style="width: 300px; height: auto;">
                        <p>Posted: ${formattedDate}</p>
                        <button class="follow" data-post-id="${post.pk}">${isFollowing ? 'Unfollow' : 'Follow'}</button>
                        <button class="like" data-post-id="${post.pk}">${isLiked ? 'Unlike' : 'Like'}</button>
                        <a class="nav-link" href="/comments/${post.pk}">Comments</a>
                        <hr>
                    `;
                    container.appendChild(postDiv);
                });
                

                const likeButtons = document.querySelectorAll('.like');
                likeButtons.forEach(button => {
                    button.addEventListener('click', function() {
                      const postId = this.getAttribute('data-post-id');
                      const isLiked = this.textContent.trim().toLowerCase() === 'unlike'; 
                  
                      fetch(`/like_post/${postId}`)
                        .then(response => response.json())
                        .then(data => {
        
                            console.log('Post', isLiked ? 'unliked' : 'liked');
           
                            this.textContent = isLiked ? 'Like' : 'Unlike';
                          
                        })
                        .catch(error => {
                          console.error('Error:', error);
                        });
                    });
                  });
                  
                const followButtons = document.querySelectorAll('.follow');
                followButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        const postId = this.getAttribute('data-post-id');
                        const isFollowing = this.textContent.trim().toLowerCase() === 'unfollow'; 

                        fetch(`/follow/${postId}`)
                            .then(response => response.json())
                            .then(data => {

                                console.log('Post', isFollowing ? 'unfollowed' : 'followed');
           
                                this.textContent = isFollowing ? 'Follow' : 'Unfollow';
                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                    });
                });
            })
            .catch(error => {
                console.error('Error:', error.message);
            });
    }
    loadPosts();
});