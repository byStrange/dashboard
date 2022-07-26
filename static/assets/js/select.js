var options = document.querySelectorAll(".quiz .option"),
  toggleFullScreen = document.querySelector("#toggleFullScreen"),
  quizBox = document.querySelector(".quiz-box");
toggleFullScreen.onclick = function (ev) {
  this.querySelector("svg").classList.toggle("mini");
  quizBox.classList.toggle("zoomIn");
};
options.forEach((option) => {
  option.onclick = function () {
    options.forEach(
      (o) => (o.classList.remove("checked"), o.removeAttribute("data-checked"))
    );
    this.classList.add("checked"), this.setAttribute("data-checked", true);
  };
});

