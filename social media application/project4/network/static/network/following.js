document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('#feed');
    let loadedPosts = 0;
    const postsPerPage = 10;

    function loadPosts() {
        fetch(`/following/${postsPerPage}/${loadedPosts}`)
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
                        <p>Owner: <a href="/other_profile_page/${post.fields.owner}">${post.fields.owner_name || ''}</a></p>
                        <img src="${post.fields.picture_link}" alt="Post Image" style="width: 300px; height: auto;">
                        <p>Posted: ${formattedDate}</p>
                        <button class="follow" data-post-id="${post.pk}">${isFollowing ? 'Unfollow' : 'Follow'}</button>
                        <button class="like" data-post-id="${post.pk}">${isLiked ? 'Unlike' : 'Like'}</button>
                        <a class="nav-link" href="/comments/${post.pk}">Comments</a>
                        <hr>
                    `;
                    container.appendChild(postDiv);
                });
                

                loadedPosts += parsedPosts.length;

                if (parsedPosts.length < postsPerPage) {
                    window.removeEventListener('scroll', loadMorePosts);
                }

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

    function loadMorePosts() {
        if ((window.innerHeight + Math.round(window.scrollY)) >= document.body.offsetHeight) {
            loadPosts();
        }
    }

    window.addEventListener('scroll', loadMorePosts);

    loadPosts();
});

