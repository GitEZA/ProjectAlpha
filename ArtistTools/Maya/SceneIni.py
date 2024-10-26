import os
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from maya import cmds
import maya.mel as mel


# designer.exeで作ったUIファイルを取得する
CURRENT_FILE = os.path.normpath(__file__)
path, ext = os.path.splitext(CURRENT_FILE)
UI_FILE = path + ".ui"

## MainWindowを作るクラス
class MainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # UIのパスを指定
        self.UI = QUiLoader().load(UI_FILE)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle(self.UI.windowTitle())
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        self.UI.FolderSelectButton.clicked.connect(self.FolderSelectButton)
        self.UI.SceneIniButton.clicked.connect(self.SceneIniButton)
        #フォルダパスを保存するための変数
        self.folder_path = ""

    def FolderSelectButton(self):
        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            # 選択したフォルダのパスをラインエディットに表示
            self.UI.lineEdit2.setText(self.folder_path)


    def SceneIniButton(self):
        input_text = self.UI.lineEdit.text()
        base_folder = self.folder_path + "/" + input_text

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            print(f"ベースフォルダが作成されました: {self.folder_path}")


        FOLDER_STRUCTURE = {
            input_text: {
                "Maya": {
                    "sourceImage":{},
                    "scene":{},
                    "fbx":{}
                },
                "SubstancePainter": {
                    "fbx":{}
                },
                "SubstanceDesigner":{
                    "fbx":{}
                },
                "Houdini":{
                    "fbx":{}
                }
            }
        }

        # 各フォルダを作成
        def create_subfolders(current_path, structure):
            for folder_name, subfolders in structure.items():
                # フォルダパスを生成
                folder_path = os.path.join(current_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                print(f"フォルダが作成されました: {folder_path}")
                
                # サブフォルダがある場合、さらに再帰的に作成
                if isinstance(subfolders, dict):
                    create_subfolders(folder_path, subfolders)
    
        # ルートフォルダ内に階層構造を作成
        create_subfolders(self.folder_path, FOLDER_STRUCTURE)

        # 1. 新規シーンを作成
        cmds.file(new=True, force=True)
        print("新しいシーンが作成されました")

        # 2. workspace.mel ファイルを特定のフォルダに作成
        workspace_file_path = os.path.join(base_folder, "workspace.mel")
        
        with open(workspace_file_path, "w") as file:
            # 必要な内容をworkspace.melに記述
            file.write("// Example workspace.mel file\n")
            file.write("workspace -fr \"images\" \"images\";\n")
            file.write("workspace -fr \"scenes\" \"scenes\";\n")
            print(f"workspace.mel ファイルが作成されました: {workspace_file_path}")
        
        # 3. ワークスペースを適用
        cmds.workspace(base_folder, openWorkspace=True)
        print(f"ワークスペースが適用されました: {base_folder}")

