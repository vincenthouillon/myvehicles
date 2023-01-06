window.addEventListener("load", () => {
  if (document.querySelector(".js-preloader") !== null) {
    document.querySelector(".js-preloader").classList.add("fade-out");
    setTimeout(() => {
      document.querySelector(".js-preloader").style.display = "none";
    }, 600);
  }
});

// Closes the navbar when clicked outside
window.onload = function () {
  document.addEventListener("click", function (event) {
    // if the clicked element isn't child of the navbar, you must close it if is open
    if (
      !event.target.closest("#navbarMesVehicules") &&
      document.getElementById("navbar").classList.contains("show")
    ) {
      document.getElementById("menu_button").click();
    }
  });
};
