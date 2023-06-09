// Get the dropdown content
var dropdownContent = document.getElementById("dropdown");

// Toggle the dropdown content when the user clicks on the username
document.querySelector(".dropbtn").addEventListener("click", function() {
  dropdownContent.classList.toggle("show");
});

// Hide the dropdown content when the user clicks outside of it
window.addEventListener("click", function(event) {
  if (!event.target.matches(".dropbtn") && !event.target.matches(".dropdown-content")) {
    dropdownContent.classList.remove("show");
  }
});