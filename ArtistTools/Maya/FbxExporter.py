# -*- coding: utf-8 -*-
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
        self.UI.ExportButton.clicked.connect(self.ExportButton)
        relative_folder = "Maya/fbx"
        project_dir = cmds.workspace(query=True, rootDirectory=True)
        self.output_folder = project_dir + relative_folder

    def ExportButton(self):
        
        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            cmds.warning("エクスポートするオブジェクトが選択されていません。")
            return
        obj_name = selected_objects[0]
        
        output_file_path = os.path.join(self.output_folder, f"{obj_name}.fbx")
        # Windowsのパスセパレータを修正
        output_file_path = output_file_path.replace('\\', '/')
        
        mel.eval('FBXExportSmoothingGroups -v true')
        mel.eval('FBXExportTangents -v true')
        mel.eval('FBXExportSkins -v true')
        mel.eval('FBXExportShapes -v true')

        cmds.select(obj_name)
        mel.eval(f'FBXExport -f "{output_file_path}" -s')
        print(f"FBXファイルがエクスポートされました: {output_file_path}")

