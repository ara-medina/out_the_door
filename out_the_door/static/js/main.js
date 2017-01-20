// var outTheDoor = function() {
    
//     this.profileList = $("#profile-list");
//     // Compile the profile list template from the HTML file
//     this.profileListTemplate = Handlebars.compile($("#profile-list-template").html());
    
//     this.profiles = [];
//     // Get the current list of uploaded profiles
//     this.getProfiles();
// };

// outTheDoor.prototype.getProfiles = function() {
//     // Make a get request to list all of the profiles
//     var ajax = $.ajax('/api/profiles', {
//         type: 'GET',
//         dataType: 'json'
//     });
    
//     // add arguments here
//     ajax.done();
//     ajax.fail();
// };

// outTheDoor.prototype.onGetProfilesDone = function(data) {
//     // Update the profiles array, and update the user interface
//     this.profiles = data;
//     this.updateProfileView();
// };

// outTheDoor.prototype.updateProfileView = function() {
//     // Render the handlebars template for the profile list, and insert it into
//     // the DOM
//     var context = {
//         profiles: this.profiles
//     };

//     var profileList = $(this.profileListTemplate(context));
//     this.profileList.replaceWith(profileList);
//     this.profileList = profileList;
// };

// outTheDoor.prototype.onFail = function(what, event) {
//     // Called when an AJAX call fails
//     console.error(what, "failed: ", event.statusText);
// };

// $(document).ready(function() {
//     window.app = new outTheDoor();
// });




// // <form method="POST" role="form">
// //     <div class="form-group">
// //         <label for="title">Caption</label>
// //         <input type="text" class="form-control" id="caption" name="caption" placeholder="Caption" required>
// //     </div>
// //     <div class="form-group">
// //         <label for="content">Occupation</label>
// //         <input type="text" class="form-control" id="occupation" name="occupation" placeholder="Occupation">
// //     </div>
// //     <button type="submit" class="btn btn-default">Submit</button>
// // </form>