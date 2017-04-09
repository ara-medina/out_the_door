var outTheDoor = function() {

    $("#newPhotoButton").on("click touchstart", function() {
        $("#photoSuccessMsg").css("display", "none");
        $("#file-input").trigger("click");
    });
    
    $("#file-input").on("click touchstart", function() {
        $("#photoSuccessMsg").css("display", "none");
    });

    // When the get post button is clicked call the onGetPost function
    $("#getPostButton").on("click touchstart", this.onGetPost.bind(this));
    
    // When the save post button is clicked call the onPostCreateButtonClicked function
    $("#postModal").on("click touchstart", "#postButton",
                  this.onPostCreateButtonClicked.bind(this));
    
    // When the edit post button is clicked call the onPostEditButtonClicked function
    $("#postModal").on("click touchstart", "#editPostButton",
                  this.onPostEditButtonClicked.bind(this));
                  
    // When the edit post button is clicked call the onPostEditButtonClicked function
    $("#postModal").on("click touchstart", "#deletePostButton",
                  this.onPostDeleteButtonClicked.bind(this));
    
    // When the save account button is clicked call the onAccountCreateButtonClicked function
    $("#createAccountModal").on("click touchstart", "#createAccountButton",
                  this.onAccountCreateButtonClicked.bind(this));
                  
    // When the login button is clicked call the onLoginButtonClicked function
    $("#loginModal").on("click touchstart", "#loginButton",
                  this.onLoginButtonClicked.bind(this));
                  
    // When the logout button is clicked call the onLogoutButtonClicked function
    $("#logoutAgree").on("click touchstart", this.onLogoutButtonClicked.bind(this));
    
    // When the user selects a file call the onFileAdded function
    this.fileInput = $("#file-input");
    this.fileInput.change(this.onFileAdded.bind(this));
                   
    this.postModal = $("#postModal");
    this.accountForm = $("#createAccountModal");
    this.loginForm = $("#loginModal");
    this.postList = $("#postList");
    this.postForm = $("#postForm");
                   
    // Compile the post list template from the HTML file
    this.postListTemplate = Handlebars.compile($("#post-list-template").html());

    this.posts = [];
    this.post = [];
    this.accounts = [];
    this.photos = [];
    this.photo = [];
    
    // Get the current list of uploaded posts
    this.getPosts();
};

// LOGIN FUNCTIONS

outTheDoor.prototype.onLoginButtonClicked = function(event) {
    
    // Create a data object from the upload form
    var data = {
        username: $('#loginUsername').val(),
        password: $('#loginPassword').val()
    };
    
    // Make a POST request to the login endpoint
    var ajax = $.ajax('/api/login', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json',
        error: function (xhr) {
            alert(xhr.responseText);
            $('#loginModal').modal('toggle');
            // fix for backdrop not closing on submit or exit
            $("#loginButton, #loginClose").click(function(){
                $(".modal-backdrop").remove();
            });
        }
    });
    

    ajax.done(this.onLoginDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Login clicked"));
};

outTheDoor.prototype.onLoginDone = function(data) {
    this.getPosts();
    
    // if the user previously created a post, fetch that post 
    if (data["post"]) {
        var postId = data["post"]["id"];
        this.onGetPost(postId);
    };
        
    $("#logoutButton").css("display","inline-block");
    $(".fa-pencil").css("display","inline-block");
    $(".fa-user").css("display","none");
    
};

// LOGOUT FUNCTIONS
outTheDoor.prototype.onLogoutButtonClicked = function(event) {
    // Make a POST request to the logout endpoint
    var ajax = $.ajax('/api/logout');

    ajax.done(this.onLogoutDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Logout clicked"));
};

outTheDoor.prototype.onLogoutDone = function(data) {
    this.getPosts();
    
    $("#logoutButton").css("display","none");
    $(".fa-pencil").css("display","none");
    $("#postButton").css("display","block");
    $("#editPostButton").css("display","none");
    $("#deletePostButton").css("display","none");
    $(".fa-user").css("display","inline-block");
    
    document.getElementById("caption").value = "";
    document.getElementById("age").value = "";
    document.getElementById("genderSelect").value = "";
    document.getElementById("ethnicitySelect").value = "";
    document.getElementById("city").value = "";
    document.getElementById("profession").value = "";
    document.getElementById("file-input").value = "";
    
    $("#file-input").css("display","block");
    $("#fileHelp").css("display","block");
    $("#newPhotoButton").css("display","none");
    
};

// ACCOUNT FUNCTIONS

outTheDoor.prototype.onAccountCreateButtonClicked = function(event) {
    
    // Create a data object from the upload form
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
        contentType: 'application/json',
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.responseText);
        }
    });
    
    ajax.done(this.onCreateAccountDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Create account"));
    
};

outTheDoor.prototype.onCreateAccountDone = function(data) {
    // Add the account to the accounts array, and display success message
    this.accounts.push(data);
    $(".alert").show();
    $(".alert").on("click touchstart", "#loginAlert", function() {
        $(".alert").hide();
        $('#loginModal').modal('show');
    });
    
    $("#postButton").css("display","block");
};

// FILE FUNCTIONS


outTheDoor.prototype.onFileAdded = function(event) {
    console.log("onFileAdded");
    var file = this.fileInput[0].files[0];
    var data = new FormData(this.postForm[0]);
    
    this.getSignedRequest(file, data);
}

outTheDoor.prototype.getSignedRequest = function(file, data) {
    console.log("getSignedRequest");
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                outTheDoor.prototype.s3FileUpload(file, data, response.data, response.url);
                console.log(data);
            }
            else{
                console.log("Could not get signed URL.");
            }
        }
    };
    xhr.send();
}

outTheDoor.prototype.s3FileUpload = function(file, data, s3Data, url) {
    console.log("s3FileUpload");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data.url);
    
    var data = new FormData();
    for(key in s3Data.fields){
        data.append(key, s3Data.fields[key]);
    }
    data.append('file', file);
    
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4){
          if(xhr.status === 200 || xhr.status === 204){
            console.log("File upload successful");
            outTheDoor.prototype.fileUpload(data, s3Data);
          }
          else{
            console.log("S3 File upload failed");
          }
        }
        };
    xhr.send(data);
};

outTheDoor.prototype.fileUpload = function(data, s3Data) {
    console.log("fileUpload");
    
    // Make a POST request to the file upload endpoint
    var ajax = $.ajax('/api/files', {
        type: 'POST',
        xhr: this.createUploadXhr.bind(this),
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        dataType: 'json'
    });
    ajax.done(this.onFileUploadDone.bind(this));
    ajax.fail(this.onFail.bind(this, "File upload"));
}

outTheDoor.prototype.createUploadXhr = function() {
    console.log("createUploadXhr");
    // XHR file upload 
    var xhr = new XMLHttpRequest();
    if(xhr.upload) { // if upload property exists
        xhr.upload.addEventListener('progress',
                                    this.onUploadProgress.bind(this), false);
    }
    return xhr;
};

outTheDoor.prototype.onUploadProgress = function(event) {
    console.log("onUploadProgress");
};

// PHOTO FUNCTIONS 

outTheDoor.prototype.onFileUploadDone = function(data, s3Data) {
    console.log("onFileUploadDone");
    // Called if the file upload succeeds
    data = {
        file: {
            id: data.id,
            name: data.name,
            path: "https://outthedoor-east.s3.amazonaws.com/" + data.name
        }
    }
    
    // Make a POST request to add the photo
    var ajax = $.ajax('/api/photos', {
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'json'
    });
    ajax.done(this.onAddPhotoDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Adding photo"));
};

outTheDoor.prototype.onAddPhotoDone = function(data) {
    console.log("onAddPhotoDone");
    // Add the photo to the photos array, and then set this.photo variable to 
    // data to use in creating a post
    window.app.photos.push(data);
    window.app.photo = data;
    
    console.log(window.app.photo);
    
    $('#photoSuccessMsg').css('display', 'block');
};

outTheDoor.prototype.onGetPhoto = function(id) {
    console.log("onGetPhoto");
    // Make a get request to get a single photo
    var ajax = $.ajax('/api/photos/' + id, {
        type: 'GET',
        dataType: 'json'
    });
    
    ajax.done(this.onGetPhotoDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Getting single photo information"));
};

outTheDoor.prototype.onGetPhotoDone = function(data) {
    console.log("onGetPhotoDone");
    this.photo = data;
};

// POST FUNCTIONS

outTheDoor.prototype.getPosts = function() {
    
    // Make a get request to list all of the posts
    var ajax = $.ajax('/api/posts', {
        type: 'GET',
        dataType: 'json'
    });
    
    ajax.done(this.onGetPostsDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Getting posts information"));
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
    ajax.fail(this.onFail.bind(this, "Getting single post information"));
};

outTheDoor.prototype.onGetPostDone = function(data) {
    this.post = data;
    
    $("#editPostButton").css("display","block");
    $("#deletePostButton").css("display","block");
    $("#postButton").css("display","none");
    
    
    document.getElementById("caption").value = data["caption"];
    document.getElementById("age").value = data["age"];
    document.getElementById("genderSelect").value = data["gender"];
    document.getElementById("ethnicitySelect").value = data["ethnicity"];
    document.getElementById("city").value = data["city"];
    document.getElementById("profession").value = data["profession"];
    
    $("#file-input").css("display","none");
    $("#fileHelp").css("display","none");
    $("#newPhotoButton").css("display","block");
   
};

outTheDoor.prototype.onPostCreateButtonClicked = function(event) {
    
    // handling age data; parsing into integer if provided
    var age = parseInt($('#age').val())

    console.log(this.photo);
    
    // Create a data object from the upload form
    var data = {
        photo: {
            id: this.photo.id,
            file: {
                id: this.photo.file.id,
                name: this.photo.file.name,
                path: this.photo.file.path
            }
        },
        caption: $('#caption').val(),
        age: age,
        gender: $("#genderSelect").val(),
        ethnicity: $('#ethnicitySelect').val(),
        city: $('#city').val(),
        profession: $('#profession').val()
    };
    
    console.log(data);

    // Make a POST request to the file upload endpoint
    var ajax = $.ajax('/api/posts', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    ajax.done(this.onAddPostDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Create post"));
};

outTheDoor.prototype.onAddPostDone = function(data) {
    // Add the post to the posts array, and update the user interface
    this.posts.push(data);
    this.updatePostView();
    
    var postId = data["id"];
    this.onGetPost(postId);
    
    $("#photoSuccessMsg").css("display", "none");
    
};

outTheDoor.prototype.onPostEditButtonClicked = function(id) {

    var id = this.post['id']
    
    var age = $('#age').val();
    
    // Create a data object from the upload form
    // add photo here
    var data = {
       photo: {
            id: this.photo.id,
            file: {
                id: this.photo.file.id,
                name: this.photo.file.name,
                path: this.photo.file.path
            }
        },
        caption: $('#caption').val(),
        age: parseInt(age),
        gender: $('#genderSelect').val(),
        ethnicity: $('#ethnicitySelect').val(),
        city: $('#city').val(),
        profession: $('#profession').val()
    };


    // Make a POST request to the post edit endpoint
    var ajax = $.ajax('/api/post/' + id + '/edit', {
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    ajax.done(this.onEditPostDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Edit post"));
};

outTheDoor.prototype.onEditPostDone = function(data) {
    
    //Once edit request has been made, get the new set of posts with updated content
    this.getPosts();
};

outTheDoor.prototype.onPostDeleteButtonClicked = function(id) {
    
    // Delete a post
    var id = this.post['id'];
    
    var ajax = $.ajax('/api/posts/' + id, {
        type: 'DELETE',
        dataType: 'json'
    });
    
    document.getElementById("caption").value = "";
    document.getElementById("age").value = "";
    document.getElementById("genderSelect").value = "";
    document.getElementById("ethnicitySelect").value = "";
    document.getElementById("city").value = "";
    document.getElementById("profession").value = "";
    document.getElementById("file-input").value = "";
    
    $("#editPostButton").css("display","none");
    $("#deletePostButton").css("display","none");
    $("#postButton").css("display","block");
    
    $("#file-input").css("display","block");
    $("#fileHelp").css("display","block");
    $("#newPhotoButton").css("display","none");
    
    ajax.done(this.onDeletePostDone.bind(this));
    ajax.fail(this.onFail.bind(this, "Delete post"));
};

outTheDoor.prototype.onDeletePostDone = function(data) {
    this.getPosts();
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
    
    this.setCardHeight();
};

outTheDoor.prototype.setCardHeight = function() {
    $( window ).load(function() {
        $('.w3-content').each(function(){
            var cardHeight = $(this).children('.card1').height();
            $(this).children('.card2').height(cardHeight);
        })
    });
}

// COMMON FUNCTIONS

outTheDoor.prototype.onFail = function(what, event) {
    // Called when an AJAX call fails
    console.error(what, "failed: ", event.statusText);
};

$(document).ready(function() {
    window.app = new outTheDoor();
});
