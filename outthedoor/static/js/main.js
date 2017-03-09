var outTheDoor = function() {

    this.postList = $("#post-list");
    console.log(this.postList);
    
    // When the save post button is clicked call the onPostSaveButtonClicked function
    $("#postModal").on("click", "#post-button",
                   this.onPostSaveButtonClicked.bind(this));
                   
    this.postForm = $("#post-modal");
                   
    // Compile the post list template from the HTML file
    this.postListTemplate = Handlebars.compile($("#post-list-template").html());
    this.posts = [];
    // Get the current list of uploaded posts
    this.getPosts();
};

outTheDoor.prototype.getPosts = function() {
    // Make a get request to list all of the posts
    var ajax = $.ajax('/api/posts', {
        type: 'GET',
        dataType: 'json'
    });
    
    ajax.done(this.onGetPostsDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Getting post information"));
};

outTheDoor.prototype.onGetPostsDone = function(data) {
    // Update the posts array, and update the user interface
    this.posts = data;
    this.updatePostView();
};

outTheDoor.prototype.onPostSaveButtonClicked = function(event) {
    console.log('called onPostSaveButtonClicked');
    
    // Create a FormData object from the upload form
    var data = {
        caption: $('#caption').val()
    };
 
    
    // Make a POST request to the file upload endpoint
    var ajax = $.ajax('/api/posts', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    ajax.done(this.onAddPostDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
};

outTheDoor.prototype.onAddPostDone = function(data) {
    // Add the post to the posts array, and update the user interface
    this.posts.push(data);
    this.updatePostView();
};

outTheDoor.prototype.updatePostView = function() {
    // Render the handlebars template for the post list, and insert it into
    // the DOM
    var context = {
        posts: this.posts
    };

    var postList = $(this.postListTemplate(context));
    this.postList.replaceWith(postList);
    this.postList = postList;
};

outTheDoor.prototype.onFail = function(what, event) {
    // Called when an AJAX call fails
    console.error(what, "failed: ", event.statusText);
};

$(document).ready(function() {
    console.log("hello");
    window.app = new outTheDoor();
});




// <form method="POST" role="form">
//     <div class="form-group">
//         <label for="title">Caption</label>
//         <input type="text" class="form-control" id="caption" name="caption" placeholder="Caption" required>
//     </div>
//     <div class="form-group">
//         <label for="content">Occupation</label>
//         <input type="text" class="form-control" id="occupation" name="occupation" placeholder="Occupation">
//     </div>
//     <button type="submit" class="btn btn-default">Submit</button>
// </form>