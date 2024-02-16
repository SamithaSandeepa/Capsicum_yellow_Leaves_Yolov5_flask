// scripts.js
document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("image-upload-form")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      var formData = new FormData(this);
      console.log(formData);

      fetch("/detect", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          displayResults(data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });

  function displayResults(results) {
    var resultsContainer = document.getElementById("results-container");
    resultsContainer.innerHTML = "";

    results.forEach((result) => {
      var card = document.createElement("div");
      card.className = "col-md-4 mb-3";
      card.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${result.image_name}</h5>
                        <ul>
                            ${result.detection_results
                              .map(
                                (det) =>
                                  `<li>${det.name} - Confidence: ${det.confidence}</li>`
                              )
                              .join("")}
                        </ul>
                    </div>
                </div>
            `;
      resultsContainer.appendChild(card);
    });
  }
});
