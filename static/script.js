// // Add event listener to the theme toggle button
// document.getElementById('theme-toggle').addEventListener('click', function() {
//     const body = document.body;
//     const toggleButton = document.getElementById('toggle-btn_image');

//     // Toggle between light and dark themes
//     body.classList.toggle('theme--light');
//     body.classList.toggle('theme--dark');

//     // Update image source based on theme
//     if (body.classList.contains('theme--dark')) {
//         toggleButton.src = "/static/images/dark-toggle.png";
//     } else {
//         toggleButton.src = "/static/images/light-toggle.png";
//     }
// });
document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const toggleButton = document.getElementById('theme-toggle');
    const toggleButtonImage = document.getElementById('toggle-btn_image');

    // Check the saved theme in local storage
    if (localStorage.getItem('theme') === 'dark') {
      body.classList.add('theme--dark');
      body.classList.remove('theme--light');
      toggleButtonImage.src = "/static/images/dark-toggle.png";
    } else {
      body.classList.add('theme--light');
      body.classList.remove('theme--dark');
      toggleButtonImage.src = "/static/images/light-toggle.png";
    }

    // Add event listener to the theme toggle button
    toggleButton.addEventListener('click', function() {
      // Toggle between light and dark themes
      body.classList.toggle('theme--light');
      body.classList.toggle('theme--dark');

      // Update image source based on theme
      if (body.classList.contains('theme--dark')) {
        toggleButtonImage.src = "/static/images/dark-toggle.png";
        localStorage.setItem('theme', 'dark');
      } else {
        toggleButtonImage.src = "/static/images/light-toggle.png";
        localStorage.setItem('theme', 'light');
      }
    });
  });