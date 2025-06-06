let button = document.querySelector("#search-button");

button.addEventListener("click", doSubmission);
console.log("done");

function doSubmission() {
  let greenIns = [];
  let yellowIns = [];
  for (let i = 1; i <= 5; i++) {
    let yi = document.querySelector(`#yellow${i}-in`);
    let gi = document.querySelector(`#green${i}-in`);
    greenIns.push(gi.value);
    yellowIns.push(yi.value);
  }
  console.log(greenIns, yellowIns);

  let grayIn = document.querySelector("#gray-in");
  let grays = grayIn.value;

  let url = URL.parse("search", window.location.toString());
  for (let i = 0; i < 5; i++) {
    url.searchParams.set(`g${i + 1}`, greenIns[i]);
    url.searchParams.set(`y${i + 1}`, yellowIns[i]);
  }
  url.searchParams.set("grays", grays);

  console.log(url);

  fetch(url)
    .then((resp) => resp.text())
    .then((text) => {
      let r = document.querySelector("#results");
      r.innerHTML = text;
    });
}
