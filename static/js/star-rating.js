document.addEventListener("DOMContentLoaded", function () {
  const stars = document.querySelectorAll("#starRating .star");
  const hiddenInput = document.getElementById("id_stars_given");
  const starRating = document.getElementById("starRating");

  // 1️⃣ Avvalgi bahoni olish
  const currentValue = starRating.getAttribute("data-current");

  if (currentValue) {
    stars.forEach(star => {
      if (star.getAttribute("data-value") <= currentValue) {
        star.classList.add("selected");
      }
    });
  }

  // 2️⃣ Keyingi clicklar uchun event listenerlar
  stars.forEach(star => {
    star.addEventListener("click", function () {
      const value = this.getAttribute("data-value");
      hiddenInput.value = value;

      stars.forEach(s => {
        s.classList.toggle("selected", s.getAttribute("data-value") <= value);
      });
    });

    star.addEventListener("mouseover", function () {
      const value = this.getAttribute("data-value");
      stars.forEach(s => {
        s.classList.toggle("hover", s.getAttribute("data-value") <= value);
      });
    });

    star.addEventListener("mouseout", function () {
      stars.forEach(s => s.classList.remove("hover"));
    });
  });
});
