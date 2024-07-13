function handleOpenFile(object) {
  var file = object.files[0];
  var reader = new FileReader();
  reader.onload = function () {
    document.getElementById("editor").innerHTML = reader.result;
  };
  reader.readAsText(file);
}

function handleSaveFile() {
  // данные, которые нужно сохранить в файл
  const data = document.getElementById("editor").value;
  // создаем объект Blob для данных
  const blob = new Blob([data], { type: "text/plain" });

  // создаем ссылку для скачивания файла
  const url = URL.createObjectURL(blob);

  // создаем ссылку для скачивания файла
  const a = document.createElement("a");
  a.href = url;
  a.download = ".env";
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
}

function handleLaunchBot() {}
