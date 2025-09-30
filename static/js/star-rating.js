document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll("#starRating .star");
  const hiddenInput = document.getElementById("id_stars_given");

  stars.forEach(star => {
    star.addEventListener("click", function () {
      const value = this.getAttribute("data-value");
      hiddenInput.value = value;

      // Tanlangan yulduzchalarni bo‘yash
      stars.forEach(s => {
        s.classList.toggle("selected", s.getAttribute("data-value") <= value);
      });
    });

    star.addEventListener("mouseover", function () {
      const value = this.getAttribute("data-value");

      // Hover bo‘lganda vaqtincha bo‘yash
      stars.forEach(s => {
        s.classList.toggle("hover", s.getAttribute("data-value") <= value);
      });
    });

    star.addEventListener("mouseout", function () {
      // Hover olib tashlash
      stars.forEach(s => s.classList.remove("hover"));
    });
  });
});
