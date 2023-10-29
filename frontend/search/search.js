document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");
  const searchResults = document.getElementById("search-results");

  searchForm.addEventListener("submit", function (event) {
    event.preventDefault(); // �y�[�W�̍ēǂݍ��݂�h�~

    const searchTerm = searchInput.value;
    if (searchTerm.trim() === "") {
      return; // ��̃N�G���𖳎�
    }

    // �T�[�o�[��Ajax���N�G�X�g�𑗐M
    fetch(`/search/${searchTerm}`)
      .then((response) => response.json())
      .then((data) => {
        // �������ʂ�\�����邽�߂̏���
        searchResults.innerHTML = "";
        if (data.length === 0) {
          searchResults.innerHTML = "�Y�����郆�[�U�[��������܂���ł����B";
        } else {
          data.forEach((result) => {
            const resultElement = document.createElement("div");
            resultElement.textContent = result; // �������ʂ�K�؂ɕ\������R�[�h��ǉ�
            searchResults.appendChild(resultElement);
          });
        }
      })
      .catch((error) => {
        console.error("�����G���[:", error);
      });
  });
});
