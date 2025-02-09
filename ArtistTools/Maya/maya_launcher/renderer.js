const { ipcRenderer } = require("electron");

document.getElementById("launchMaya").addEventListener("click", () => {
    ipcRenderer.send("launch-maya", "");
});

document.getElementById("selectScript").addEventListener("click", async () => {
    let file = await ipcRenderer.invoke("open-file-dialog");
    if (file) {
        ipcRenderer.send("launch-maya", file);
        document.getElementById("status").innerText = `✅ スクリプト選択: ${file}`;
    }
});

// Maya の起動ステータスを表示
ipcRenderer.on("launch-status", (event, message) => {
    document.getElementById("status").innerText = message;
});
