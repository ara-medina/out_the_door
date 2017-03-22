var outTheDoor = function() {
    
    $('#logoutPopover').popover({
        html:true,
        trigger: 'hover'
    });
    
    this.postList = $("#post-list");
    
    // When the save post button is clicked call the onPostSaveButtonClicked function
    $("#postModal").on("click", "#post-button",
                  this.onPostSaveButtonClicked.bind(this));
    
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
                   
    // Compile the post list template from the HTML file
    this.postListTemplate = Handlebars.compile($("#post-list-template").html());
    this.posts = [];
    this.accounts = [];
    // Get the current list of uploaded posts
    this.getPosts();
};

// POST FUNCTIONS

outTheDoor.prototype.getPosts = function() {
    console.log("called getPosts");
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
    
    var age = $('#age').val();
    
    // var income = document.getElementById("incomeSelect").value;
    // console.log(income);
    
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
    
    console.log(data)
    
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


// ACCOUNT FUNCTIONS

outTheDoor.prototype.onAccountCreateButtonClicked = function(event) {
    console.log('called onAccountCreateButtonClicked');
    
    // Create a FormData object from the upload form
    var data = {
        username: $('#accountUsername').val(),
        firstname: $('#accountFirstName').val(),
        lastname: $('#accountLastName').val(),
        email: $('#accountEmail').val(),
        password: $('#accountPassword').val()
    };
    
    console.log(data)
    
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
    console.log("success!");
    this.accounts.push(data);
    $(".alert").show();
    $(".alert").on("click", "#login-alert", function() {
        $(".alert").hide();
        $('#loginModal').modal('show');
    });
};

// LOGIN FUNCTIONS

outTheDoor.prototype.onLoginButtonClicked = function(event) {
    console.log('called onLoginButtonClicked');
    
    // Create a FormData object from the upload form
    var data = {
        username: $('#loginUsername').val(),
        password: $('#loginPassword').val()
    };
    
    console.log(data)
    
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
    console.log("success!");
    this.getPosts();
    
    $("#logoutPopover").css("display","block")
    
};

// LOGOUT FUNCTIONS
outTheDoor.prototype.onLogoutButtonClicked = function(event) {
    console.log('called onLogoutButtonClicked');

     
    // Make a POST request to the logout endpoint
    var ajax = $.ajax('/api/logout');


    ajax.done(this.onLogoutDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
};

outTheDoor.prototype.onLogoutDone = function(data) {
    console.log("logged out");
    this.getPosts();
    
    $("#logoutPopover").css("display","none")
    
};

// COMMON FUNCTIONS

outTheDoor.prototype.onFail = function(what, event) {
    // Called when an AJAX call fails
    console.error(what, "failed: ", event.statusText);
};

$(document).ready(function() {
    window.app = new outTheDoor();
});
