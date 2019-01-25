'''
Created on 8/04/2016

@author: jagir
'''

from alignimages_ui import Ui_MainWindow
from opencmiss.zinc.context import Context
from opencmiss.zinc.element import Element, Elementbasis
from opencmiss.zinc.field import Field


from PySide import QtGui, QtCore
from PySide.QtGui import QApplication

import sys, ntpath, Image, os, traceback,pickle
from Aligner import DicomConvertor

class Aligner(QtGui.QMainWindow,Ui_MainWindow):
    '''
    UI to help manually align a set of images
    '''
    zscale = 1000
    filenameMap = dict()
    tablerowMap = dict()
    zincSurfaces = dict()
    filebrowseActive = False
    imageMetaData = dict()
    sliceNodes = dict()
    zincContext = Context('Align')
    graphicsInitialized = False
    spinex = 0
    spiney = 0
    spineNodes = None
    dicomConvertor = DicomConvertor.Convertor()
    
    def __init__(self):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.xLocation.setText( '%g' % (self.spinex))
        self.yLocation.setText( '%g' % (self.spiney))
        self.zincViewer.setContext(self.zincContext)
        
        self.fileNames.cellChanged.connect(self.updatePosition)
        
        self.loadFiles.clicked.connect(self.browse)
        self.zincViewer.graphicsInitialized.connect(self.sceneinit)
        self.viewAll.clicked.connect(self.zincViewer.viewAll)
        self.showX.clicked.connect(self.setLabel)
        self.showY.clicked.connect(self.setLabel)
        self.showZ.clicked.connect(self.setLabel)
        self.xLocation.textChanged.connect(self.showSpine)
        self.yLocation.textChanged.connect(self.showSpine)
        self.save.clicked.connect(self.saveAsDicomFiles)
        self.actionSave.triggered.connect(self.saveState)
        self.actionLoad.triggered.connect(self.loadState)
    

    def saveState(self):
        dataDetails = dict()
        rowPosition = self.fileNames.rowCount()
        if rowPosition > 0:
            for row in range(rowPosition):  
                mx = float(self.fileNames.item(row,1).text())
                my = float(self.fileNames.item(row,2).text())
                mz = float(self.fileNames.item(row,3).text())
                visible = self.fileNames.item(row,4).checkState() == QtCore.Qt.CheckState.Checked
                dataDetails[row] = [self.tablerowMap[row],mx,my,mz,visible]
            dataDetails['spinelocation'] = [self.spinex,self.spiney]
            filename = str(QtGui.QFileDialog.getSaveFileName(self,'File to save current setup')[0])
            if not filename.endswith(".pickle"):
                filename = '%s.pickle' %(filename)
            try:
                with open(filename,'wb+') as ser:
                    pickle.dump(dataDetails, ser, -1)
            except:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText("Error occured while saving file %s" %(filename))
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QtGui.QMessageBox.Ok)
                msg.exec_()
        else:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
        
            msg.setText("No files have been loaded!!")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
        
    def loadState(self):
        #If something is loaded, then cant do
        if len(self.zincSurfaces) > 0:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
        
            msg.setText("Cannot load files when current state has images")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
            return
        
        filename = str(QtGui.QFileDialog.getOpenFileName(self,'File to load setup')[0])
        self.filebrowseActive = True
        try:
            with open(filename,'rb') as ser:
                dataDetails = pickle.load(ser)

                numRows = len(dataDetails) -1
                for i in range(numRows):
                    val = dataDetails[i]
                    filen = val[0]
                    mx = val[1]
                    my = val[2]
                    mz = val[3]
                    visble = val[4]
                    try:
                        jpgfile = Image.open(filen)
                    except:
                        jpgfile = None
                        
                    if jpgfile is  None:
                        continue
                    self.imageMetaData[i] = (jpgfile.size[0],jpgfile.size[1],0)
                    name =ntpath.basename(filen)
                    try:
                        if not self.filenameMap.has_key(name):
                            
                            self.filenameMap[name] = [filen,i]
                            self.tablerowMap[i] = filen
                            self.fileNames.insertRow(i)
                            self.fileNames.setItem(i , 0, QtGui.QTableWidgetItem(name))
                            item = QtGui.QTableWidgetItem()
                            item.setData(QtCore.Qt.EditRole, mx)
                            self.fileNames.setItem(i , 1, item)
                            item = QtGui.QTableWidgetItem()
                            item.setData(QtCore.Qt.EditRole, my)
                            self.fileNames.setItem(i , 2, item)
                            item = QtGui.QTableWidgetItem()
                            item.setData(QtCore.Qt.EditRole, mz)
                            self.fileNames.setItem(i , 3, item)
                            item = QtGui.QTableWidgetItem()
                            if visble:
                                item.setCheckState(QtCore.Qt.Checked)
                            else:
                                item.setCheckState(QtCore.Qt.Unchecked)
                            self.fileNames.setItem(i , 4, item)
                            
                            #Show the image in zinc
        
                            self.createSurface(i)
                            self.loadTextureFromFile(i, self.zincViewer,visble)
                            #Update offsets
                            if mx!=0.0 or mx!=0.0 or mz !=0.0:
                                nodeHandles,x,y,_,fieldModule,fieldCache,coordinateField = self.sliceNodes[i]
                                #Z is not image property
                                pts = [[mx,my,mz],[x+mx,my,mz],[mx,y+my,mz],[x+mx,y+my,mz]]
                                fieldModule.beginChange()
                                for j,nid in enumerate(nodeHandles):
                                    fieldCache.setNode(nodeHandles[nid])
                                    coordinateField.assignReal(fieldCache,list(pts[j]))
                                    
                                fieldModule.endChange()
                            if not visble:
                                self.zincSurfaces[i][0].beginChange() #scene
                                self.zincSurfaces[i][1].setVisibilityFlag(visble) # Points
                                self.zincSurfaces[i][2].setVisibilityFlag(visble) # Lines
                                self.zincSurfaces[i][3].setVisibilityFlag(visble) # Surfaces
                                self.zincSurfaces[i][0].endChange()

                    except:
                        traceback.print_exc(file=sys.stdout)
                
                val = dataDetails['spinelocation']
                #This will trigger show Spine 
                self.xLocation.setText( '%g' % (val[0]))
                self.yLocation.setText( '%g' % (val[1]))

                #self.showSpine()
                self.zincViewer.viewAll()
        except:
            traceback.print_exc(file=sys.stdout)
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText("Error occured while loading file %s" %(filename))
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.exec_()
            
        self.filebrowseActive = False
        self.actionLoad.setEnabled(False)
    
    def sceneinit(self):
        self.graphicsInitialized = True
    
    #Find files
    def browse(self):
        file_dialog = QtGui.QFileDialog(self)
        # the name filters must be a list
        file_dialog.setNameFilters(["Images (*.png *.jpg *.tif)"])
        file_dialog.selectNameFilter("Images (*.png *.jpg *.tif)")
        # show the dialog
        file_dialog.exec_()
        #List of selected files
        filename = file_dialog.selectedFiles()
        for filen in filename:
            try:
                jpgfile = Image.open(filen)
            except:
                jpgfile = None
                
            if jpgfile is  None:
                continue
            
            rowPosition = self.fileNames.rowCount()
            self.imageMetaData[rowPosition] = (jpgfile.size[0],jpgfile.size[1],0)
            name =ntpath.basename(filen)
            try:
                if not self.filenameMap.has_key(name):
                    self.filebrowseActive = True
                    self.filenameMap[name] = [filen,rowPosition]
                    self.tablerowMap[rowPosition] = filen
                    self.fileNames.insertRow(rowPosition)
                    self.fileNames.setItem(rowPosition , 0, QtGui.QTableWidgetItem(name))
                    item = QtGui.QTableWidgetItem()
                    item.setData(QtCore.Qt.EditRole, 0)
                    self.fileNames.setItem(rowPosition , 1, item)
                    item = QtGui.QTableWidgetItem()
                    item.setData(QtCore.Qt.EditRole, 0)
                    self.fileNames.setItem(rowPosition , 2, item)
                    item = QtGui.QTableWidgetItem()
                    item.setData(QtCore.Qt.EditRole, rowPosition*self.zscale)
                    self.fileNames.setItem(rowPosition , 3, item)
                    item = QtGui.QTableWidgetItem()
                    item.setCheckState(QtCore.Qt.Checked)
                    self.fileNames.setItem(rowPosition , 4, item)
                    
                    #Show the image in zinc

                    self.createSurface(rowPosition)
                    self.loadTextureFromFile(rowPosition, self.zincViewer)
                    self.showSpine()
                    self.zincViewer.viewAll()

            except:
                traceback.print_exc(file=sys.stdout)
                
                 
        self.filebrowseActive = False 
        if len(self.zincSurfaces) > 0 :
            self.actionLoad.setEnabled(False)


    def createSurface(self,rowPosition):
        '''
        Creates an element with appropriate coords
        '''
        parentRegionName= 'image%d' % (rowPosition)
        (x,y,z) = self.imageMetaData[rowPosition]
        z += rowPosition*self.zscale
        #Create a square element
        defaultRegion = self.zincContext.getDefaultRegion().createChild(parentRegionName)
        
        
        fieldModule = defaultRegion.getFieldmodule()
        fieldCache = fieldModule.createFieldcache()
        coordinateField = fieldModule.createFieldFiniteElement(3)
        # Set the name of the field, we give it label to help us understand it's purpose
        coordinateField.setName('coordinates')
        coordinateField.setTypeCoordinate(True)
        xfield = fieldModule.createFieldComponent(coordinateField, 1)
        xfield.setName("x")
        xfield.setManaged(True)
        yfield = fieldModule.createFieldComponent(coordinateField, 2)
        yfield.setName("y")
        yfield.setManaged(True)
        zfield = fieldModule.createFieldComponent(coordinateField, 3)
        zfield.setName("z")
        zfield.setManaged(True)
        # Find a special node set named 'cmiss_nodes'
        nodeset = fieldModule.findNodesetByName('nodes')
        nodeTemplate = nodeset.createNodetemplate()
        # Set the finite element coordinate field for the nodes to use
        nodeTemplate.defineField(coordinateField)
        
        nodeHandles = dict()
        pts = [[0,0,z],[x,0,z],[0,y,z],[x,y,z]]
        fieldModule.beginChange()
        for nid in range(4):
            pt = pts[nid]
            node = nodeset.createNode(nid+1, nodeTemplate)
            fieldCache.setNode(node)
            coordinateField.assignReal(fieldCache,list(pt))
            nodeHandles[nid] = node
        
        self.sliceNodes[rowPosition] = (nodeHandles,x,y,z,fieldModule,fieldCache,coordinateField)
        #Create edges
        mesh = fieldModule.findMeshByDimension(2)
        elementTemplate = mesh.createElementtemplate()
        elementTemplate.setElementShapeType(Element.SHAPE_TYPE_SQUARE)
        element_node_count = 4
        elementTemplate.setNumberOfNodes(element_node_count)
        # Specify the dimension and the interpolation function for the element basis function. 
        linear_basis = fieldModule.createElementbasis(2, Elementbasis.FUNCTION_TYPE_LINEAR_LAGRANGE)
        # The indexes of the nodes in the node template we want to use
        linear_node_indexes = [1, 2, 3, 4]
        elementTemplate.defineFieldSimpleNodal(coordinateField, -1, linear_basis, linear_node_indexes)
        for nid in range(4):
            elementTemplate.setNode(nid+1, nodeHandles[nid])
        mesh.defineElement(-1, elementTemplate)        
        
        fieldModule.endChange()
        
        fieldModule.defineAllFaces()
        
        self.imageMetaData[rowPosition] = (x,y,z,xfield,yfield,zfield,coordinateField,defaultRegion,fieldModule)
        
    def setLabel(self):
        senderLabel = str(self.sender().text())
        self.showX.setEnabled(True)
        self.showY.setEnabled(True)
        self.showZ.setEnabled(True)
        if senderLabel == 'X':
            for data in self.imageMetaData:
                _,_,_,xfield,_,_,_,_,_,_,gnodes = self.imageMetaData[data]
                attrib = gnodes.getGraphicspointattributes()
                attrib.setLabelField(xfield)
        elif senderLabel == 'Y':
            for data in self.imageMetaData:
                _,_,_,_,yfield,_,_,_,_,_,gnodes = self.imageMetaData[data]
                attrib = gnodes.getGraphicspointattributes()
                attrib.setLabelField(yfield)

        elif senderLabel == 'Z':
            for data in self.imageMetaData:
                _,_,_,_,_,zfield,_,_,_,_,gnodes = self.imageMetaData[data]
                attrib = gnodes.getGraphicspointattributes()
                attrib.setLabelField(zfield)
            
            
        self.sender().setEnabled(False)
        
    def loadTextureFromFile(self,rowPosition,sceneviewer,visble=True):

        x,y,z,xfield,yfield,zfield,coordinateField,defaultRegion,fieldModule = self.imageMetaData[rowPosition]
        filen = self.tablerowMap[rowPosition]
        # Create an image field. A temporary xi source field is created for us.
        imageField = fieldModule.createFieldImage()
        #To handle large images create the texture coordinates
        xiField = fieldModule.findFieldByName('xi')
        constField = fieldModule.createFieldConstant([x,y,1])
        textureCoordinates = fieldModule.createFieldMultiply(xiField,constField) 

        imageField.setTextureCoordinateSizes([x, y, 1])
        # Create a stream information object that we can use to read the
        # image file from disk
        stream_information = imageField.createStreaminformationImage()
        stream_information.setFileFormat(stream_information.FILE_FORMAT_JPG)
        stream_information.createStreamresourceFile(str(filen))

        imageField.read(stream_information)
        
        scene = defaultRegion.getScene()
        image = scene.getMaterialmodule().createMaterial()
        image.setManaged(True)
        image.setName('texture%d' % (rowPosition))
        image.setTextureField(1, imageField)
        #image.setAttributeReal(Material.ATTRIBUTE_ALPHA, 1)

        
        
        scene.beginChange()
        lines = scene.createGraphicsLines()
        lines.setCoordinateField(coordinateField)
        
        gnodes = scene.createGraphicsPoints()
        gnodes.setCoordinateField(coordinateField)
        gnodes.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
        attrib = gnodes.getGraphicspointattributes()
        attrib.setLabelField(xfield)

        surfaces = scene.createGraphicsSurfaces()
        surfaces.setCoordinateField(coordinateField)
        surfaces.setTextureCoordinateField(textureCoordinates)
        surfaces.setMaterial(image)
        if not visble:
            gnodes.setVisibilityFlag(False)
            lines.setVisibilityFlag(False)
            surfaces.setVisibilityFlag(False)
        scene.endChange()
        
        self.zincSurfaces[rowPosition] = [scene, gnodes, lines,surfaces]
        
        self.imageMetaData[rowPosition] = (x,y,z,xfield,yfield,zfield,coordinateField,defaultRegion,fieldModule,scene,gnodes)

    def getZRange(self):
        rowPosition = self.fileNames.rowCount()
        minz = 1e+200
        maxz = -minz
        for row in range(rowPosition):  
            mz = float(self.fileNames.item(row,3).text())
            if minz > mz:
                minz = mz
            if maxz < mz:
                maxz = mz
        return (minz-self.zscale,maxz+self.zscale)

    def showSpine(self):
        try:
            x = float(self.xLocation.text())
        except:
            x = self.spinex
        self.spinex = x
        try:
            y = float(self.yLocation.text())
        except:
            y = self.spiney
        self.spiney = y

        minz,maxz = self.getZRange()
        if self.spineNodes is not None:
            nodeHandles,fieldModule,fieldCache,coordinateField = self.spineNodes
            pts = [[self.spinex,self.spiney,minz],[self.spinex,self.spiney,maxz]]
            fieldModule.beginChange()
            for i,nid in enumerate(nodeHandles):
                pt = pts[i]
                fieldCache.setNode(nodeHandles[nid])
                coordinateField.assignReal(fieldCache,list(pt))
            fieldModule.endChange()
        else:
            
            
            defaultRegion = self.zincContext.getDefaultRegion()
            fieldModule = defaultRegion.getFieldmodule()
            fieldCache = fieldModule.createFieldcache()
            coordinateField = fieldModule.createFieldFiniteElement(3)
            # Set the name of the field, we give it label to help us understand it's purpose
            coordinateField.setName('coordinates')
            coordinateField.setTypeCoordinate(True)
            # Find a special node set named 'cmiss_nodes'
            nodeset = fieldModule.findNodesetByName('nodes')
            nodeTemplate = nodeset.createNodetemplate()
            # Set the finite element coordinate field for the nodes to use
            nodeTemplate.defineField(coordinateField)
            
            nodeHandles = dict()
            pts = [[self.spinex,self.spiney,minz],[self.spinex,self.spiney,maxz]]
            fieldModule.beginChange()
            for nid in range(2):
                pt = pts[nid]
                node = nodeset.createNode(nid+1, nodeTemplate)
                fieldCache.setNode(node)
                coordinateField.assignReal(fieldCache,list(pt))
                nodeHandles[nid] = node
        
            self.spineNodes = (nodeHandles,fieldModule,fieldCache,coordinateField)
            #Create edges
            mesh = fieldModule.findMeshByDimension(1)
            elementTemplate = mesh.createElementtemplate()
            elementTemplate.setElementShapeType(Element.SHAPE_TYPE_LINE)
            element_node_count = 2
            elementTemplate.setNumberOfNodes(element_node_count)
            # Specify the dimension and the interpolation function for the element basis function. 
            linear_basis = fieldModule.createElementbasis(1, Elementbasis.FUNCTION_TYPE_LINEAR_LAGRANGE)
            # The indexes of the nodes in the node template we want to use
            linear_node_indexes = [1, 2]
            elementTemplate.defineFieldSimpleNodal(coordinateField, -1, linear_basis, linear_node_indexes)
            for nid in range(2):
                elementTemplate.setNode(nid+1, nodeHandles[nid])
            mesh.defineElement(-1, elementTemplate)        
            
            fieldModule.endChange()
            x,y,_,_,_,_,_,_,_,_,_ = self.imageMetaData[0]
            scene = defaultRegion.getScene()
            scene.beginChange()
            lines = scene.createGraphicsLines()
            lines.setCoordinateField(coordinateField)
            attrib = lines.getGraphicslineattributes()
            attrib.setShapeType(attrib.SHAPE_TYPE_CIRCLE_EXTRUSION)
            attrib.setBaseSize([x*0.1,y*0.1,10])
            scene.endChange()
        
                
    def updatePosition(self,row,col):
        if not self.filebrowseActive:
            if col > 0 and col < 4:
                nodeHandles,x,y,_,fieldModule,fieldCache,coordinateField = self.sliceNodes[row]
                mx = float(self.fileNames.item(row,1).text())
                my = float(self.fileNames.item(row,2).text())
                mz = float(self.fileNames.item(row,3).text())
                #Z is not image property
                pts = [[mx,my,mz],[x+mx,my,mz],[mx,y+my,mz],[x+mx,y+my,mz]]
                fieldModule.beginChange()
                for i,nid in enumerate(nodeHandles):
                    fieldCache.setNode(nodeHandles[nid])
                    coordinateField.assignReal(fieldCache,list(pts[i]))
                    
                fieldModule.endChange()
            else:
                value = self.fileNames.item(row,col).checkState() == QtCore.Qt.CheckState.Checked
                self.zincSurfaces[row][0].beginChange() #scene
                self.zincSurfaces[row][1].setVisibilityFlag(value) # Points
                self.zincSurfaces[row][2].setVisibilityFlag(value) # Lines
                self.zincSurfaces[row][3].setVisibilityFlag(value) # Surfaces
                self.zincSurfaces[row][0].endChange()
                
            self.showSpine()
            self.zincViewer.viewAll()
            
    def saveAsDicomFiles(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, 'Select Output Location')
        try:
            if os.path.isdir(directory):
                rowPosition = self.fileNames.rowCount()
                for i in range(rowPosition):
                    filename = str(self.fileNames.item(i,0).text())
                    ox = float(self.fileNames.item(i,1).text())
                    oy = float(self.fileNames.item(i,2).text())
                    oz = float(self.fileNames.item(i,3).text())
                    imagefile = os.path.join(directory,os.path.splitext(filename)[0]+".dcm")
                    
                    self.dicomConvertor.convert(self.tablerowMap[i], imagefile, ox, oy, oz)
                    
        except:
            print 'Error while saving '
            traceback.print_exc(file=sys.stdout)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Aligner()
    w.show()
    try:
        app.exec_()
    except:
        pass
