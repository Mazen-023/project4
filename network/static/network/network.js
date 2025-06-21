document.addEventListener('DOMContentLoaded', function() {
    
    // Load posts
    load_posts();
    
    // Create post
    document.querySelector("#post_form").addEventListener('submit', create);
});

function load_posts() {
    fetch('/read')
    .then(response => response.json())
    .then(posts => {
        posts.forEach(function(post) {

            // Create new post
            let div = document.createElement('div');
            div.className = 'post';
            div.innerHTML = `
            <div class="post_header">
                <div>
                    <strong>${post.user.username}</strong>
                    <span>${post.timestamp}</span>
                </div>
                <div class="post_actions">
                    <a href="#">Edit</a>
                </div>
            </div>
            <p>${post.content}</p>
            <div class="post_footer">                
                <i class="bi bi-hand-thumbs-up"></i> Like
            </div>
            `

            document.querySelector('.posts').append(div);

            // Add event listener for the edit link
            div.querySelector('.post_actions a').addEventListener('click', function() {
                // Handle edit post
            });

            // Add event listener for the like button
            div.querySelector('.post_footer').addEventListener('click', function() {
                // Handle like post
            });

        });
    })
    .catch(error => {
        console.log('Error:', error);
    });

}

function create() {
    fetch('/create', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#post_content').value,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.log('Error:', error);
    });
}