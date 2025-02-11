const { ipcRenderer } = require("electron");

// ボタンが存在するか確認してイベントを設定
const addIpcListener = (buttonId, channel) => {
    const button = document.getElementById(buttonId);
    if (button) {
        button.addEventListener("click", () => {
            try {
                ipcRenderer.send(channel);
                console.log(`📢 ${channel} を送信しました`);
            } catch (error) {
                console.error(`❌ ${channel} の送信エラー: ${error.message}`);
            }
        });
    } else {
        console.warn(`⚠ ボタンが見つかりません: ${buttonId}`);
    }
};

// 各ボタンにイベントを登録
addIpcListener("launchMaya", "launch-maya");
addIpcListener("launchUnreal", "launch-Unreal");
addIpcListener("launchHoudini", "launch-Houdini");
addIpcListener("launchPainter", "launch-Painter");
addIpcListener("launchDesigner", "launch-Designer");


// Maya の起動ステータスを表示
ipcRenderer.on("launch-status", (event, message) => {
    document.getElementById("status").innerText = message;
});
