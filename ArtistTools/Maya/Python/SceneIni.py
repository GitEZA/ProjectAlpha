import os
from os import rename
from traceback import print_tb

from PySide6 import QtWidgets, QtUiTools, QtCore
from PySide6.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from maya import cmds
import maya.mel as mel

# QtDesigner.exeで作ったUIファイルを取得する
CURRENT_FILE = os.path.normpath(__file__)
path, ext = os.path.splitext(CURRENT_FILE)
UI_FILE = path + ".ui"

mesh_types = {
    "SM：プロップ": "SM",
    "SK：キャラクター": "SK"
}

## MainWindowを作るクラス
class MainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # UIのパスを指定
        loader = QUiLoader()
        self.ui = loader.load(UI_FILE, self)
        self.setWindowTitle(self.ui.windowTitle())
        self.setCentralWidget(self.ui)

        # ウィジェットを取得
        self.folder_path = ""

        # ボタンのイベント接続
        self.ui.FolderSelectButton.clicked.connect(self.FolderSelectButton)
        self.ui.SceneIniButton.clicked.connect(self.SceneIniButton)

        self.comboBoxType = self.ui.findChild(QtWidgets.QComboBox, "comboBoxType")
        self.comboBoxType.clear()
        self.comboBoxType.addItems(mesh_types.keys())


    def FolderSelectButton(self):
        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            # 選択したフォルダのパスをラインエディットに表示
            self.ui.lineEdit2.setText(self.folder_path)

    def SceneIniButton(self):
        input_text = self.ui.lineEdit.text()
        mesh_type = mesh_types.get(self.ui.comboBoxType.currentText(), "SM")
        self.folder_name = mesh_type + "_" + input_text
        base_folder = os.path.join(self.folder_path, self.folder_name)

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        folder_structure = {
            self.folder_name: {
                "Maya": {
                    "sourceImage": {},
                    "scene": {},
                    "fbx": {}
                },
                "SubstancePainter": {
                    "fbx": {}
                },
                "SubstanceDesigner": {
                    "fbx": {}
                },
                "Houdini": {
                    "fbx": {}
                }
            }
        }

        # 各フォルダを作成
        def create_subfolders(current_path, structure):
            for folder_name, subfolders in structure.items():
                folder_path = os.path.join(current_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                print(f"フォルダが作成されました: {folder_path}")

                if isinstance(subfolders, dict):
                    create_subfolders(folder_path, subfolders)

        create_subfolders(self.folder_path, folder_structure)

        # 1. 新規シーンを作成
        cmds.file(new=True, force=True)

        cmds.spaceLocator(n=self.folder_name, p=(1, 1, 1))
        cmds.group(em=True, n='Work')
        cmds.group(em=True, n=self.folder_name + "_Base", p='Work')
        cmds.group(em=True, n=self.folder_name + "_low", p='Work')
        cmds.group(em=True, n=self.folder_name + "_high", p='Work')
        cmds.group(em=True, n="Shelf", p='Work')

        print("新しいシーンが作成されました")

        # 2. workspace.mel ファイルを作成
        workspace_file_path = os.path.join(base_folder, "workspace.mel")

        with open(workspace_file_path, "w") as file:
            file.write("// Example workspace.mel file\n")
            file.write("workspace -fr \"images\" \"images\";\n")
            file.write("workspace -fr \"scenes\" \"scenes\";\n")
            print(f"workspace.mel ファイルが作成されました: {workspace_file_path}")

        # 3. ワークスペースを適用
        cmds.workspace(base_folder, openWorkspace=True)
        print(f"ワークスペースが適用されました: {base_folder}")

        # 4. シーンの保存
        project_dir = cmds.workspace(query=True, rootDirectory=True)
        save_name = self.folder_name + ".mb"
        relative_folder = "Maya/scene/" + save_name
        save_path = os.path.join(project_dir, relative_folder)

        cmds.file(rename=save_path)
        cmds.file(save=True, type='mayaBinary', force=True)
        print(f"シーンが保存されました: {save_path}")



def closeEvent(self, event):
    super().closeEvent(event)


def main():
    window = MainWindow()
    window.show()

if __name__ == "__main__":
    main()

