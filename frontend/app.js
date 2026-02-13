const API_URL='http://localhost:5000';

const postForm=document.getElementById('postForm');
const postsContainer=document.getElementById('postsContainer');

async function fetchPosts()
{
    const response = await fetch(API_URL + '/posts');
    const posts = await response.json();
    
    postsContainer.innerHTML='';

    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className= 'post-card';
        postDiv.innerHTML = `
                            <h3>${post[1]}</h3>
                            <p class="author">By: ${post[2]}</p>
                            <p class="content">${post[3]}</p>
                            <small>${post[4]}</small>
                            <button class="delete-btn" onclick="deletePost(${post[0]})">Delete</button>
        `;
        postsContainer.appendChild(postDiv);
    });
}

async function createPost(event)
{
    event.preventDefault();

    const title=document.getElementById('title').value;
    const author=document.getElementById('author').value;
    const content=document.getElementById('content').value;

    const response= await fetch(API_URL + '/posts' ,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({title,author,content})
    }
    );
    postForm.reset();
    fetchPosts();
}

async function deletePost(id)
{
    if(confirm('Are you sure you want to delete this post?'))
    {
        await fetch(API_URL + '/posts/' +id,{
            method: 'DELETE'
        });
        fetchPosts();
    }
}

postForm.addEventListener('submit',createPost);
fetchPosts();