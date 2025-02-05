import os
from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import cmds

# designer.exeで作ったUIファイルを取得する
CURRENT_FILE = os.path.normpath(__file__)
path, ext = os.path.splitext(CURRENT_FILE)
UI_FILE = path + ".ui"


## MainWindowクラス（PySide6 & Maya 2025用）
class MainWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # UIのロード（PySide6の方法）
        self.UI = self.load_ui(UI_FILE)

        # ウィンドウタイトルをUIから取得
        self.setWindowTitle(self.UI.windowTitle())

        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        # UIのボタンと関数を接続
        self.UI.FolderSelectButton.clicked.connect(self.FolderSelectButton)
        self.UI.SceneIniButton.clicked.connect(self.SceneIniButton)

        # フォルダパスを保存するための変数
        self.folder_path = ""

    def load_ui(self, file_path):
        """PySide6でのUIロード"""
        loader = QUiLoader()
        ui_file = QFile(file_path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def FolderSelectButton(self):
        """フォルダ選択ダイアログ"""
        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            # 選択したフォルダのパスをラインエディットに表示
            self.UI.lineEdit2.setText(self.folder_path)

    def SceneIniButton(self):
        """シーンの初期化処理"""
        input_text = self.UI.lineEdit.text()
        base_folder = os.path.join(self.folder_path, input_text)

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f"ベースフォルダが作成されました: {self.folder_path}")

        # フォルダ構造定義
        FOLDER_STRUCTURE = {
            input_text: {
                "Maya": {
                    "sourceImage": {},
                    "scene": {},
                    "fbx": {}
                },
                "SubstancePainter": {"fbx": {}},
                "SubstanceDesigner": {"fbx": {}},
                "Houdini": {"fbx": {}}
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

        # ルートフォルダ内に階層構造を作成
        create_subfolders(self.folder_path, FOLDER_STRUCTURE)

        # 1. 新規シーンを作成
        cmds.file(new=True, force=True)
        cmds.currentUnit(linear='m')
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

        # 4.グループとロケーターの作成
        group_work = cmds.group(empty=True, name="Work")
        group_low = cmds.group(empty=True, name=input_text + "_low")
        group_high = cmds.group(empty=True, name=input_text + "_high")
        group_shelf = cmds.group(empty=True, name="Shelf")
        print(f"グループ '{group_work}''{group_low}''{group_high}''{group_shelf}'を作成しました。")

        locator_name = cmds.spaceLocator(name=input_text)[0]
        cmds.parent(group_shelf, group_work)
        cmds.parent(group_low, group_work)
        cmds.parent(group_high, group_work)
        print(f"ロケーター '{locator_name}' を作成しました。")


