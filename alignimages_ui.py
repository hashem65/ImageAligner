# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alignimages.ui'
#
# Created: Mon Apr 11 10:12:19 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileNames = QtGui.QTableWidget(self.layoutWidget)
        self.fileNames.setColumnCount(5)
        self.fileNames.setObjectName("fileNames")
        self.fileNames.setHorizontalHeaderLabels(['File','X','Y','Z','Visible'])
        self.fileNames.setRowCount(0)
        self.fileNames.horizontalHeader().setStretchLastSection(True)
        self.fileNames.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.fileNames)
        self.loadFiles = QtGui.QPushButton(self.layoutWidget)
        self.loadFiles.setObjectName("loadFiles")
        self.verticalLayout.addWidget(self.loadFiles)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.zincViewer = SceneviewerWidget(self.layoutWidget1)
        self.zincViewer.setObjectName("zincViewer")
        self.verticalLayout_2.addWidget(self.zincViewer)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.showX = QtGui.QPushButton(self.layoutWidget1)
        self.showX.setCheckable(True)
        self.showX.setObjectName("showX")
        self.horizontalLayout.addWidget(self.showX)
        self.showY = QtGui.QPushButton(self.layoutWidget1)
        self.showY.setCheckable(True)
        self.showY.setObjectName("showY")
        self.horizontalLayout.addWidget(self.showY)
        self.showZ = QtGui.QPushButton(self.layoutWidget1)
        self.showZ.setCheckable(True)
        self.showZ.setObjectName("showZ")
        self.horizontalLayout.addWidget(self.showZ)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.xLocation = QtGui.QLineEdit(self.layoutWidget1)
        self.xLocation.setObjectName("xLocation")
        self.horizontalLayout_2.addWidget(self.xLocation)
        self.yLocation = QtGui.QLineEdit(self.layoutWidget1)
        self.yLocation.setObjectName("yLocation")
        self.horizontalLayout_2.addWidget(self.yLocation)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.viewAll = QtGui.QPushButton(self.layoutWidget1)
        self.viewAll.setObjectName("viewAll")
        self.horizontalLayout_3.addWidget(self.viewAll)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.save = QtGui.QPushButton(self.layoutWidget1)
        self.save.setObjectName("save")
        self.horizontalLayout_4.addWidget(self.save)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.setStretch(0, 10)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 2)
        self.horizontalLayout_5.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Aligner", None, QtGui.QApplication.UnicodeUTF8))
        self.loadFiles.setText(QtGui.QApplication.translate("MainWindow", "Add File", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Show", None, QtGui.QApplication.UnicodeUTF8))
        self.showX.setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.showY.setText(QtGui.QApplication.translate("MainWindow", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.showZ.setText(QtGui.QApplication.translate("MainWindow", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Spine Location", None, QtGui.QApplication.UnicodeUTF8))
        self.viewAll.setText(QtGui.QApplication.translate("MainWindow", "View All", None, QtGui.QApplication.UnicodeUTF8))
        self.save.setText(QtGui.QApplication.translate("MainWindow", "Save Dicoms", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))

#from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget
from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget
