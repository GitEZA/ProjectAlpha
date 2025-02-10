const { ipcRenderer } = require("electron");

document.getElementById("launchMaya").addEventListener("click", () => {
    ipcRenderer.send("launch-maya", "");
});
document.getElementById("launchUnreal").addEventListener("click", () => {
    ipcRenderer.send("launch-Unreal", "");
});

// Maya の起動ステータスを表示
ipcRenderer.on("launch-status", (event, message) => {
    document.getElementById("status").innerText = message;
});
