$(document).ready(() => {
  // Function to handle the change event for the father select
  function updateFatherImage() {
    let selected = $("#fatherSelect").children("option:selected").val();
    $.get(`/pigeon/get/${selected}`, (data) => {
      console.log(data);
      $("#cockImage").attr("src", data["image_url"]);
    });
  }

  // Function to handle the change event for the mother select
  function updateMotherImage() {
    let selected = $("#motherSelect").children("option:selected").val();
    $.get(`/pigeon/get/${selected}`, (data) => {
      console.log(data);
      $("#henImage").attr("src", data["image_url"]);
    });
  }

  // Attach the change event handlers to the select elements
  $("#fatherSelect").on("change", updateFatherImage);
  $("#motherSelect").on("change", updateMotherImage);

  // Call the functions initially to update the images when the page loads
  updateFatherImage();
  updateMotherImage();
});
