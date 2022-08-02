const nextBtn =
  document.querySelector("#nextQuiz") ||
  document.createElement("button");

// const prevBtn =
//   prevQuiz ||
//   document.querySelector("#prevQuiz") ||
//   document.createElement("button");

nextBtn.onclick = function () {
  var answer = document.querySelector(".option.checked");
  if (!answer) {
    alert("Please select an answer");
    return void 0;
  } else {
    answer = answer.innerText;
  }
  var data = {
    exam_slug: exam_slug,
    question_id: question_id,
    answer: answer,
    csrfmiddlewaretoken: csrf_token,
  };
  console.log(data);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      const response = JSON.parse(this.responseText);
      var { next_quiz_url } = response;
      var { exam_result_url } = response;
      if (next_quiz_url) {
        window.location.href = next_quiz_url;
      } else {
        window.location.href = exam_result_url;
      }
    }
  };
  xhttp.open(
    "GET",
    "/my/quiz/" +
      data.exam_slug +
      "/test/" +
      data.question_id +
      "/check?data=" +
      JSON.stringify(data),
  );
  xhttp.send();
};
