const { app, BrowserWindow, ipcMain } = require("electron");
const { exec } = require("child_process");
const path = require("path");

let mainWindow;

app.whenReady().then(() => {
    mainWindow = new BrowserWindow({
        width: 500,
        height: 400,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.loadFile("index.html");
});


ipcMain.on("launch-maya", () => {
    const MAYA_PATH = `"C:\\Program Files\\Autodesk\\Maya2025\\bin\\maya.exe"`;
    const PYTHON_PATH = `"C:\\GitData\\ProjectAlpha\\ArtistTools\\Maya\\Python"`;

    const command = `SET PYTHONPATH=PYTHON_PATH;C:\\GitData\\ProjectAlpha\\ArtistTools\\Maya\\Python && ${MAYA_PATH}`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`エラー: ${error.message}`);
        } else {
            console.log("✅ Maya が起動しました！", stdout);
        }
    });
});


ipcMain.on("launch-Unreal", () => {
    const uePath = "C:\\Program Files\\Epic Games\\UE_5.5\\Engine\\Binaries\\Win64\\UnrealEditor.exe";
    const projectPath = "C:\\GitData\\ProjectAlpha\\Project\\Project.uproject";

    const command = `"${uePath}" "${projectPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`エラー: ${error.message}`);
        } else {
            console.log("✅ Unreal が起動しました！", stdout);
        }
    });

});


ipcMain.on("launch-Houdini", () => {
    const houdiniPath = `"C:\\Program Files\\Side Effects Software\\Houdini 20.5.487\\bin\\houdini.exe"`;

    exec(houdiniPath, (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Houdini 起動エラー: ${error.message}\n${stderr}`);
        } else {
            console.log("✅ Houdini が起動しました！", stdout);
        }
    });
});


ipcMain.on("launch-Painter", () => {
    const painterPath = `"C:\\Program Files\\Adobe\\Adobe Substance 3D Painter\\Adobe Substance 3D Painter.exe"`;

    exec(painterPath, (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Substance 3D Painter 起動エラー: ${error.message}\n${stderr}`);
        } else {
            console.log("✅ Substance 3D Painter が起動しました！", stdout);
        }
    });
});


ipcMain.on("launch-Designer", () => {
    const designerPath = `"C:\\Program Files\\Adobe\\Adobe Substance 3D Designer\\Adobe Substance 3D Designer.exe"`;

    exec(designerPath, (error, stdout, stderr) => {
        if (error) {
            console.error(`❌ Substance 3D Designer 起動エラー: ${error.message}\n${stderr}`);
        } else {
            console.log("✅ Substance 3D Designer が起動しました！", stdout);
        }
    });
});


