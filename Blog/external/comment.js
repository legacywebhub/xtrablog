var form = document.getElementById('comment-form')
var formButton = document.getElementById('comment-button')
var post = formButton.dataset.post

form.addEventListener('submit', function(e){
  e.preventDefault();
  var comment = form.comment.value
  var url = "{% url 'Blog:post_comment' %}"

  formData = {
  'comment': comment,
  'post': post
  }

  fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'formData':formData})
      })
      .then((response)=>{
          return data = response.json()
      })
      .then((data)=>{
        console.log('success:', data)
        location.reload()
      });
});