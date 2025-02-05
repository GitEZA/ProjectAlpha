# -*- coding: utf-8 -*-
import os
from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import cmds
import maya.mel as mel

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

        # ボタンのクリックイベントを接続
        self.UI.ExportButton.clicked.connect(self.ExportButton)

        # 出力フォルダの設定
        relative_folder = "Maya/fbx"
        project_dir = cmds.workspace(query=True, rootDirectory=True)
        self.output_folder = os.path.join(project_dir,relative_folder)

    def load_ui(self, file_path):
        """PySide6でのUIロード"""
        loader = QUiLoader()
        ui_file = QFile(file_path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def ExportButton(self):
        """選択したオブジェクトをFBXとしてエクスポート"""
        selected_objects = cmds.ls(selection=True, shortNames=True)
        if not selected_objects:
            cmds.warning("エクスポートするオブジェクトが選択されていません。")
            return

        clean_names = [name.lstrip('|') for name in selected_objects]
        obj_name = clean_names[0]
        output_file_path = os.path.join(self.output_folder, f"{obj_name}.fbx")

        # Windowsのパスセパレータを修正
        output_file_path = output_file_path.replace('\\', '/')

        # FBXエクスポート設定
        mel.eval('FBXExportSmoothingGroups -v true')
        mel.eval('FBXExportTangents -v true')
        mel.eval('FBXExportSkins -v true')
        mel.eval('FBXExportShapes -v true')


        # オブジェクトを選択してエクスポート
        mel.eval(f'FBXExport -f "{output_file_path}" -s')
        print(f"FBXファイルがエクスポートされました: {output_file_path}")

