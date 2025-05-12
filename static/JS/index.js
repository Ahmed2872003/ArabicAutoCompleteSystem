const searchForm = document.querySelector("[role='search']");
const searchInput = document.getElementById("search");
const suggestionBox = document.getElementById("suggestions");

let debounceId;
const nOfSequences = 5;
const debounceTime = 400;

searchForm.onsubmit = (e) => {
  e.preventDefault();
};

searchInput.oninput = (e) => {
  let inputVal = e.target.value;

  clearTimeout(debounceId);

  if (!inputVal) return hideSuggestionsBox();

  debounceId = setTimeout(async () => {
    inputVal = inputVal.replace(/[^a-zA-Z0-9.? \u0600-\u06FF]/g, " ");

    const response = await fetch(
      `/api/v1/suggestions?input=${inputVal}&nOfSequences=${nOfSequences}`
    );

    const { suggestions } = await response.json();

    hideSuggestionsBox();

    showSuggestions(suggestions);
  }, debounceTime);
};

function showSuggestions(suggestions = []) {
  if (!suggestions.length) return;

  suggestions.forEach((suggestion) => {
    const li = document.createElement("li");
    li.textContent = suggestion;
    li.onclick = () => {
      document.getElementById("search").value = suggestion;
      suggestionBox.innerHTML = "";
      suggestionBox.style.display = "none";
    };
    suggestionBox.appendChild(li);
  });

  suggestionBox.style.display = "block";
}

async function getSuggestions(input) {}

function hideSuggestionsBox() {
  suggestionBox.innerHTML = "";
  suggestionBox.style.display = "none";
}
