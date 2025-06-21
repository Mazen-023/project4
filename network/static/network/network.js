// network.js
// This script handles the loading of posts, creating new posts, and managing post interactions.

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
            div.dataset.id = post.id;
            div.innerHTML = `
            <div class="post_header">
                <div>
                    <strong>${post.user}</strong>
                    <span>${post.timestamp}</span>
                </div>
                <div class="post_actions">
                    <a href="#">Edit</a>
                </div>
            </div>
            <p>${post.content}</p>
            <div class="post_footer">                
                <i class="bi bi-hand-thumbs-up"></i>
                <span data-id="${post.id}">${post.likes}</span>
            </div>
            `

            document.querySelector('.posts').append(div);

            // Add event listener for the edit link
            div.querySelector('.post_actions a').addEventListener('click', function() {
                edit(post.id, post.content)
            });

            // Add event listener for the like button
            div.querySelector('.post_footer').addEventListener('click', function() {
                like(post.id);
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

function edit(postId, content) {
    let div = document.querySelector(`div[data-id="${postId}"]`);
    let p = div.querySelector('p');
    let textarea = document.createElement('textarea');
    textarea.className = "form-control content";
    textarea.innerHTML = content;
    
    p.replaceWith(textarea)

}

function update(postId, content) {
    fetch(`/update/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .catch(error => {
        console.log("Error:", error);
    });
}

function like(postId) {
    fetch(`/like/${postId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        const post = document.querySelector(`div[data-id="${postId}"]`)
        const likeSpan = post.querySelector('.post_footer span');
        if (likeSpan) {
            likeSpan.innerHTML = result["likes"];
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}