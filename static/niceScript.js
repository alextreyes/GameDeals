document.addEventListener("DOMContentLoaded", () => {
  const addToListButtons = document.querySelectorAll(".add-to-list-btn");

  addToListButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // If user is logged in, toggle the display of the dropdown
      // Get the deal ID associated with the clicked button
      const dealId = button.getAttribute("data-deal-id");

      // Find the corresponding dropdown menu by its unique identifier
      const dropdownMenu = document.getElementById(`dropdown-${dealId}`);

      // Toggle the display of the dropdown menu
      dropdownMenu.style.display =
        dropdownMenu.style.display === "none" ? "block" : "none";

      // If user is not logged in, show a message or perform another action
    });
  });
});
