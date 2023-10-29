document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  searchForm.addEventListener("submit", function (event) {
    event.preventDefault(); // ページの再読み込みを防止

    const searchTerm = searchInput.value;
    if (searchTerm.trim() === "") {
      return; // 空のクエリを無視
    }

    // サーバーにAjaxリクエストを送信
    fetch(`/search/${searchTerm}`)
      .then((response) => response.json())
      .then((data) => {
        // 検索結果を表示するための処理
        searchResults.innerHTML = "";
        if (data.length === 0) {
          searchResults.innerHTML = "該当するユーザーが見つかりませんでした。";
        } else {
          data.forEach((result) => {
            const resultElement = document.createElement("div");
            resultElement.textContent = result; // 検索結果を適切に表示するコードを追加
            searchResults.appendChild(resultElement);
          });
        }
      })
      .catch((error) => {
        console.error("検索エラー:", error);
      });
  });
});
