let button = document.querySelector("#search-button");

button.addEventListener("click", doSubmission);
console.log("done");

let greenInputs = [];
let yellowInputs = [];
let grayInput = document.querySelector("#gray-in");

document.onreadystatechange = function () {
  if (document.readyState == "complete") {
    for (let i = 1; i <= 5; i++) {
      yellowInputs.push(document.querySelector(`#yellow${i}-in`));
      greenInputs.push(document.querySelector(`#green${i}-in`));
    }

    for (let idx = 0; idx < 5; idx++) {
      let inelt = greenInputs[idx];
      inelt.addEventListener("keydown", function (event) {
        console.log(event.key);
        if (event.key == "Backspace") {
          greenInputs[(idx - 1 + 5) % 5].focus();
        }
      });
      inelt.addEventListener("input", function () {
        // if (this.value.length > 1) {
        //   this.value = this.value.charAt(this.value.length - 1);
        // }
        if (this.value.length == 1) {
          if (this.value == " ") {
            this.value = "";
          }
          greenInputs[(idx + 1) % 5].focus();
        }
      });

      inelt.addEventListener("keypress", function (event) {
        if (event.key == "Enter") button.click();
      });
    }

    for (let y of yellowInputs) {
      y.addEventListener("keypress", function (event) {
        if (event.key == "Enter") button.click();
      });
    }

    grayInput.addEventListener("keypress", function (event) {
      if (event.key == "Enter") button.click();
    });
  }
};

function doSubmission() {
  let greenIns = [];
  let yellowIns = [];
  for (let i = 1; i <= 5; i++) {
    let yi = yellowInputs[i - 1];
    let gi = greenInputs[i - 1];
    greenIns.push(gi.value);
    yellowIns.push(yi.value);
  }

  let grays = grayInput.value;

  let url = URL.parse("search", window.location.toString());
  for (let i = 0; i < 5; i++) {
    url.searchParams.set(`g${i + 1}`, greenIns[i]);
    url.searchParams.set(`y${i + 1}`, yellowIns[i]);
  }
  url.searchParams.set("grays", grays);

  fetch(url)
    .then((resp) => resp.json())
    .then((obj) => {
      let container = document.querySelector("#results");
      let cDiv = document.querySelector("#pos-count");
      if (obj.status != 200) {
        container.innerHTML = "ERROR: INVALID REQUEST";
        cDiv.innerHTML = "ERR";
        return;
      }
      let words = obj.result.words;
      let count = words.length;
      cDiv.innerHTML = `${count}&nbsp;`;

      container.innerHTML = "";

      for (let word of words) {
        container.append(`${word}`);
        container.append(document.createElement("br"));
      }
    });
}
