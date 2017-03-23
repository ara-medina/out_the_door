var outTheDoor = function() {
    
    $('#logoutPopover').popover({
        html:true,
        trigger: 'hover'
    });
    
    // When the get post button is clicked call the onGetPost function
    $("#getPostButton").on("click", this.onGetPost.bind(this));
    
    // When the save post button is clicked call the onPostCreateButtonClicked function
    $("#postModal").on("click", "#post-button",
                  this.onPostCreateButtonClicked.bind(this));
    
    // When the edit post button is clicked call the onPostEditButtonClicked function
    $("#postModal").on("click", "#edit-post-button",
                  this.onPostEditButtonClicked.bind(this));
    
    // When the save account button is clicked call the onAccountCreateButtonClicked function
    $("#createAccountModal").on("click", "#create-account-button",
                  this.onAccountCreateButtonClicked.bind(this));
                  
    // When the login button is clicked call the onLoginButtonClicked function
    $("#loginModal").on("click", "#login-button",
                  this.onLoginButtonClicked.bind(this));
                  
    // When the logout button is clicked call the onLogoutButtonClicked function
    $("#logoutPopover").on("click", this.onLogoutButtonClicked.bind(this));
                   
    this.postForm = $("#post-modal");
    this.accountForm = $("#create-account-modal");
    this.loginForm = $("#login-modal");
    this.postList = $("#post-list");
                   
    // Compile the post list template from the HTML file
    this.postListTemplate = Handlebars.compile($("#post-list-template").html());

    this.posts = [];
    this.post = [];
    this.accounts = [];
    
    // Get the current list of uploaded posts
    this.getPosts();
};

// LOGIN FUNCTIONS

outTheDoor.prototype.onLoginButtonClicked = function(event) {
    // Create a FormData object from the upload form
    var data = {
        username: $('#loginUsername').val(),
        password: $('#loginPassword').val()
    };
    
    // Make a POST request to the login endpoint
    var ajax = $.ajax('/api/login', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    ajax.done(this.onLoginDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
};

outTheDoor.prototype.onLoginDone = function(data) {
    this.getPosts();
    
    if (data["post"]) {
        var postId = data["post"]["id"];
        this.onGetPost(postId);
    };
        
    $("#logoutPopover").css("display","block");
    $(".fa-pencil").css("display","block");
    
};

// LOGOUT FUNCTIONS
outTheDoor.prototype.onLogoutButtonClicked = function(event) {
    // Make a POST request to the logout endpoint
    var ajax = $.ajax('/api/logout');

    ajax.done(this.onLogoutDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
};

outTheDoor.prototype.onLogoutDone = function(data) {
    this.getPosts();
    
    $("#logoutPopover").css("display","none");
    $(".fa-pencil").css("display","none");
    $("#post-button").css("display","none");
    $("#edit-post-button").css("display","none");
    
};

// ACCOUNT FUNCTIONS

outTheDoor.prototype.onAccountCreateButtonClicked = function(event) {
    // Create a FormData object from the upload form
    
    var data = {
        username: $('#accountUsername').val(),
        firstname: $('#accountFirstName').val(),
        lastname: $('#accountLastName').val(),
        email: $('#accountEmail').val(),
        password: $('#accountPassword').val()
    };
    
    // Make a POST request to the file upload endpoint
    var ajax = $.ajax('/api/accounts', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    ajax.done(this.onCreateAccountDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
};

outTheDoor.prototype.onCreateAccountDone = function(data) {
    // Add the account to the accounts array, and display success message
    this.accounts.push(data);
    $(".alert").show();
    $(".alert").on("click", "#login-alert", function() {
        $(".alert").hide();
        $('#loginModal').modal('show');
    });
    
    $("#post-button").css("display","block");
};

// POST FUNCTIONS

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

outTheDoor.prototype.onGetPost = function(id) {
    // Make a get request to get a single post
    // This gets called when a user logs in and it finds their post
    var ajax = $.ajax('/api/posts/' + id, {
        type: 'GET',
        dataType: 'json'
    });
    
    ajax.done(this.onGetPostDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Getting post information"));
};

outTheDoor.prototype.onGetPostDone = function(data) {
    this.post = data;
    
    $("#edit-post-button").css("display","block");
    $("#post-button").css("display","none");
    
    document.getElementById("caption").value = data["caption"];
    document.getElementById("age").value = data["age"];
    document.getElementById("gender").value = data["gender"];
    document.getElementById("ethnicity").value = data["ethnicity"];
    document.getElementById("city").value = data["city"];
    document.getElementById("profession").value = data["profession"];
    document.getElementById("incomeSelect").value = data["income"];
};

outTheDoor.prototype.onPostCreateButtonClicked = function(event) {

    var age = $('#age').val();
    
    // Create a FormData object from the upload form
    var data = {
        caption: $('#caption').val(),
        age: parseInt(age),
        gender: $('#gender').val(),
        ethnicity: $('#ethnicity').val(),
        city: $('#city').val(),
        profession: $('#profession').val(),
        income: $("#incomeSelect").val()
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
    console.log("onAddPostDone");
    this.updatePostView();
    
    var postId = data["id"];
    this.onGetPost(postId);
};

outTheDoor.prototype.onPostEditButtonClicked = function(id) {

    var id = this.post['id']
    
    var age = $('#age').val();
    
    // Create a FormData object from the upload form
    var data = {
        caption: $('#caption').val(),
        age: parseInt(age),
        gender: $('#gender').val(),
        ethnicity: $('#ethnicity').val(),
        city: $('#city').val(),
        profession: $('#profession').val(),
        income: $("#incomeSelect").val()
    };

    // Make a POST request to the post edit endpoint
    var ajax = $.ajax('/api/post/' + id + '/edit', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    ajax.done(this.onEditPostDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
};

outTheDoor.prototype.onEditPostDone = function(data) {
    //Once edit request has been made, get the new set of posts with updated content
    this.getPosts();
};

outTheDoor.prototype.updatePostView = function() {
    // Render the handlebars template for the post list, and insert it into
    // the DOM
    var context = {
        posts: this.posts
    };
    
    console.log("updatePostView")

    var postList = $(this.postListTemplate(context));
    this.postList.replaceWith(postList);
    this.postList = postList;
};

// COMMON FUNCTIONS

outTheDoor.prototype.onFail = function(what, event) {
    // Called when an AJAX call fails
    console.error(what, "failed: ", event.statusText);
};

$(document).ready(function() {
    window.app = new outTheDoor();
});
