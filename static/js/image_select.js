$(document).ready(() => {
  // Function to handle the change event for the father select
  function updateFatherImage() {
    let selected = $("#fatherSelect").children("option:selected").val();
    if (selected === "") {
      // Hide the entire father card if no selection
      $("#fatherCard").hide();
    } else {
      $.get(`/pigeon/get/${selected}`, (data) => {
        console.log(data);
        $("#cockImage").attr("src", data["image_url"]); // Update the image source
        $("#fatherName").text(data["name"]); // Update the name
        $("#fatherCard").show(); // Show the entire father card
      });
    }
  }

  // Function to handle the change event for the mother select
  function updateMotherImage() {
    let selected = $("#motherSelect").children("option:selected").val();
    if (selected === "") {
      // Hide the entire mother card if no selection
      $("#motherCard").hide();
    } else {
      $.get(`/pigeon/get/${selected}`, (data) => {
        console.log(data);
        $("#henImage").attr("src", data["image_url"]); // Update the image source
        $("#motherName").text(data["name"]); // Update the name
        $("#motherCard").show(); // Show the entire mother card
      });
    }
  }

  // Attach the change event handlers to the select elements
  $("#fatherSelect").on("change", updateFatherImage);
  $("#motherSelect").on("change", updateMotherImage);

  // Call the functions initially to update the card visibility when the page loads
  updateFatherImage();
  updateMotherImage();
});
