from PyQt6.QtWidgets import QTreeWidget, QInputDialog, QHeaderView, QMessageBox
from PyQt6.QtCore import QCoreApplication
from .Functions import stringToList
from .EditWindow import EditWindow
from PyQt6.QtGui import QCursor
from .TagItem import TagItem
import nbt.region
import nbt.nbt
import zlib
import copy
import nbt
import os
import io


class TreeWidget(QTreeWidget):
    def __init__(self, env):
        super().__init__()

        self.setAcceptDrops(True)

        self.env = env
        self.NoneTag = None

        self._editWindow = EditWindow(self, env)

        self.setHeaderLabels((QCoreApplication.translate("TreeWidget", "Name"), QCoreApplication.translate("TreeWidget", "Value"), QCoreApplication.translate("TreeWidget", "Type")))
        self.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.itemDoubleClicked.connect(self.editTag)
        self.currentItemChanged.connect(self.updateMenu)

    def updateMenu(self, item: TagItem) -> None:
        if item is None:
            return
        if item.tagType() == "compound" or item.tagType() == "root" or item.tagType() == "chunk":
            self.env.mainWindow.editTagAction.setEnabled(False)
        else:
            self.env.mainWindow.editTagAction.setEnabled(True)
        if item.tagType() != "root":
            if item.parent().tagType() != "list":
                self.env.mainWindow.renameCompoundAction.setEnabled(True)
            else:
                self.env.mainWindow.renameCompoundAction.setEnabled(False)
        else:
            self.env.mainWindow.renameCompoundAction.setEnabled(False)
        if item.tagType() == "root" or item.tag_type == "chunk":
            self.env.mainWindow.removeTagAction.setEnabled(False)
        else:
            self.env.mainWindow.removeTagAction.setEnabled(True)
        self.env.mainWindow.newTagAction.setEnabled(not item.isRegionFile())
        self.env.mainWindow.newCompoundAction.setEnabled(not item.isRegionFile())
        self.env.mainWindow.newListAction.setEnabled(not item.isRegionFile())

    def newFile(self, path: str) -> None:
        rootItem = TagItem(0)
        rootItem.setText(0,os.path.basename(path))
        rootItem.setPath(path)
        rootItem.setTagType("root")
        rootItem.setFileType("nbt")
        self.addTopLevelItem(rootItem)

    def _parseNBTFile(self, nbtfile: nbt.nbt.NBTFile, path: str, file_type: str) -> None:
        rootItem = TagItem(0)
        rootItem.setText(0,os.path.basename(path))
        rootItem.setPath(path)
        rootItem.setTagType("root")
        rootItem.setFileType(file_type)
        self.parseCombound(rootItem,nbtfile)
        self.addTopLevelItem(rootItem)

    def openNBTFile(self, path: str) -> None:
        try:
            nbtfile = nbt.nbt.NBTFile(path, "rb")
            self._parseNBTFile(nbtfile, path, "nbt")
        except Exception:
            QMessageBox.critical(self, QCoreApplication.translate("TreeWidget", "Can't read file"), QCoreApplication.translate("TreeWidget", "Can't read {{path}}. Maybe it's not a NBT File.").replace("{{path}}", path))
            return

    def openRegionFile(self, path: str) -> None:
        region = nbt.region.RegionFile(path,"rb")
        rootItem = TagItem(0)
        rootItem.setText(0,os.path.basename(path))
        rootItem.setPath(path)
        rootItem.setTagType("root")
        rootItem.setFileType("region")
        for i in region.get_chunks():
            lengthItem = TagItem(rootItem)
            lengthItem.setText(0,f'X:{i["x"]}Z:{i["z"]}')
            lengthItem.setChunkCords(i["x"],i["z"])
            lengthItem.setTagType("chunk")
            lengthItem.updateTypeText()
            nbtdata = region.get_nbt(i["x"],i["z"])
            self.parseCombound(lengthItem,nbtdata)
        self.addTopLevelItem(rootItem)

    def openMccFile(self, path: str) -> None:
        try:
            with open(path, "rb") as f:
                by = f.read()

            buf = io.BytesIO(zlib.decompress(by))
            nbtfile = nbt.nbt.NBTFile(buffer=buf)
            self._parseNBTFile(nbtfile, path, "mcc")
        except Exception:
            QMessageBox.critical(self, QCoreApplication.translate("TreeWidget", "Can't read file"), QCoreApplication.translate("TreeWidget", "Can't read {{path}}. Maybe it's not a NBT File.").replace("{{path}}", path))
            return

    def parseData(self, name, value, parentItem, data):
        item = TagItem(parentItem)
        item.setText(0,name)
        if isinstance(value,nbt.nbt.TAG_Int):
            item.setTagType("int")
        elif isinstance(value,nbt.nbt.TAG_Int_Array):
            item.setTagType("int_array")
        elif isinstance(value,nbt.nbt.TAG_Long):
            item.setTagType("long")
        elif isinstance(value,nbt.nbt.TAG_Long_Array):
            item.setTagType("long_array")
        elif isinstance(value,nbt.nbt.TAG_Double):
            item.setTagType("double")
        elif isinstance(value,nbt.nbt.TAG_Float):
            item.setTagType("float")
        elif isinstance(value,nbt.nbt.TAG_Byte):
            item.setTagType("byte")
        elif isinstance(value,nbt.nbt.TAG_Byte_Array):
            item.setTagType("byte_array")
        elif isinstance(value,nbt.nbt.TAG_String):
            item.setTagType("string")
        elif isinstance(value,nbt.nbt.TAG_Short):
            item.setTagType("short")
        elif isinstance(value,nbt.nbt.TAG_Compound):
            item.setTagType("compound")
        elif isinstance(value,nbt.nbt.TAG_List):
            item.setTagType("list")
        elif value.value is None:
            item.setTagType("none")
            self.NoneTag = value
        item.updateTypeText()
        if hasattr(value,"items"):
            self.parseCombound(item,value)
        elif isinstance(value,nbt.nbt.TAG_List):
            self.parseList(item,value)
        elif  isinstance(value,nbt.nbt.TAG_Byte_Array):
            s = "["
            for i in value:
                s += f"{i},"
            s = s[:-1] + "]"
            item.setText(1,s)
        else:
            item.setText(1,str(value.value))

    def parseCombound(self, parentItem, data):
        for key, value in data.items():
            self.parseData(key,value,parentItem,data)

    def parseList(self,parentItem,data):
        for count, i in enumerate(data):
             self.parseData(str(count),i,parentItem,data)

    def saveData(self):
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.getFileType() == "nbt":
                f = nbt.nbt.NBTFile()
                self.getSaveList(item,f.tags)
                f.write_file(item.getPath())
            elif item.getFileType() == "region":
                region = nbt.region.RegionFile(item.getPath())
                for childPos in range(item.childCount()):
                    x, z = item.child(childPos).getChunkCords()
                    nbtFile = nbt.nbt.NBTFile()
                    self.getSaveList(item.child(childPos), nbtFile.tags)
                    region.write_chunk(x, z, nbtFile)
                region.close()
            elif item.getFileType() == "mcc":
                nbtfile = nbt.nbt.NBTFile()
                self.getSaveList(item, nbtfile.tags)
                buf = io.BytesIO()
                nbtfile.write_file(buffer=buf)
                buf.seek(0)
                with open(item.getPath(), "wb") as f:
                    f.write(zlib.compress(buf.read()))
            self.env.modified = False

    def getTag(self, child):
        tagType = child.tagType()
        if tagType == "int":
            data = nbt.nbt.TAG_Int(int(child.text(1)),name=child.text(0))
        elif tagType == "int_array":
            array = stringToList(child.text(1),int)
            data = nbt.nbt.TAG_Int_Array(name=child.text(0))
            data.value = array
        elif tagType == "long":
            data = nbt.nbt.TAG_Long(int(child.text(1)),name=child.text(0))
        elif tagType == "long_array":
            array = stringToList(child.text(1),int)
            data = nbt.nbt.TAG_Long_Array(name=child.text(0))
            data.value = array
        elif tagType == "double":
            data = nbt.nbt.TAG_Double(float(child.text(1)),name=child.text(0))
        elif tagType == "float":
            data = nbt.nbt.TAG_Float(float(child.text(1)),name=child.text(0))
        elif tagType == "byte":
            data = nbt.nbt.TAG_Byte(int(child.text(1)),name=child.text(0))
        elif tagType == "byte_array":
            array = stringToList(child.text(1),int)
            data = nbt.nbt.TAG_Byte_Array(name=child.text(0))
            data.value = array
        elif tagType == "string":
            data = nbt.nbt.TAG_String(child.text(1),name=child.text(0))
        elif tagType == "short":
            data = nbt.nbt.TAG_Short(int(child.text(1)),name=child.text(0))
        elif tagType == "compound":
            data = nbt.nbt.TAG_Compound()
            self.getSaveCompound(child,data)
        elif tagType == "list":
            if child.childCount() == 0:
                data = nbt.nbt.TAG_List(type=nbt.nbt.TAG_Int,name=child.text(0))
            else:
                list_tag_type = self.getTag(child.child(0)).__class__
                data =nbt.nbt.TAG_List(type=list_tag_type,name=child.text(0))
                self.getSaveList(child,data)
        elif tagType == "none":
            data = copy.copy(self.NoneTag)
        else:
            data = nbt.nbt.TAG_String("Error",name=child.text(0))
        data.name = child.text(0)
        return data

    def getSaveList(self,item,tags):
        for i in range(item.childCount()):
            child = item.child(i)
            tags.append(self.getTag(child))

    def getSaveCompound(self,item,tags):
        for i in range(item.childCount()):
            child = item.child(i)
            tag = self.getTag(child)
            tags[tag.name] = tag

    def newTag(self):
        item = self.currentItem()
        if item:
            if item.tagType() == "compound" or item.tagType() == "root":
                self._editWindow.openWindow(True,item)
            elif item.tagType() == "list":
                 self._editWindow.openWindow(True,item,taglist=True,name=str(item.childCount()))
            elif item.parent().tagType() == "list":
                 self._editWindow.openWindow(True,item.parent(),taglist=True,name=str(item.parent().childCount()))
            else:
                self._editWindow.openWindow(True,item.parent())

    def editTag(self):
        item = self.currentItem()
        if item:
            if item.tagType() != "compound" and  item.tagType() != "list" and item.tagType() != "chunk" and item.tagType() != "root":
                if item.parent().tagType() == "list":
                    self._editWindow.openWindow(False,item,taglist=True)
                else:
                    self._editWindow.openWindow(False,item)

    def newCompound(self):
        item = self.currentItem()
        if item:
            name, ok = QInputDialog.getText(self, QCoreApplication.translate("TreeWidget", "New Compound"), QCoreApplication.translate("TreeWidget", "Please enter a name for the new compound"))
            if not ok or name == '':
                return
            if item.tagType() == "compound" or item.tagType() == "list" or item.tagType() == "root":
                newComp = TagItem(item)
            else:
                newComp = TagItem(item.parent())
            newComp.setText(0,name)
            newComp.setTagType("compound")
            newComp.updateTypeText()
            self.env.modified = True

    def newList(self):
        item = self.currentItem()
        if item:
            name, ok = QInputDialog.getText(self, QCoreApplication.translate("TreeWidget", "New List"), QCoreApplication.translate("TreeWidget", "Please enter a name for the new List"))
            if not ok or name == '':
                return
            if item.tagType() == "compound" or item.tagType() == "list" or item.tagType() == "root":
                newComp = TagItem(item)
            else:
                newComp = TagItem(item.parent())
            newComp.setText(0,name)
            newComp.setTagType("list")
            newComp.updateTypeText()
            self.env.modified = True

    def renameItem(self):
        item = self.currentItem()
        if item:
            name, ok = QInputDialog.getText(self, QCoreApplication.translate("TreeWidget", "Rename"), QCoreApplication.translate("TreeWidget", "Please enter a new Name"), text=item.text(0))
            if ok and name != '':
                item.setText(0,name)
                self.env.modified = True

    def removeTag(self):
        item = self.currentItem()
        if item:
            if item.tagType() != "root":
                parent = item.parent()
                parent.removeChild(item)
                self.env.modified = True
                if parent.tagType() == "list":
                    for count,i in enumerate(range(parent.childCount())):
                        child = parent.child(i)
                        child.setText(0,str(count))

    def clearItems(self):
        for i in range(self.topLevelItemCount()):
            self.takeTopLevelItem(i)

    def contextMenuEvent(self, event):
        self.env.mainWindow.tagMenu.popup(QCursor.pos())

    def dropEvent(self, event):
        event.accept()
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            path = mimeData.urls()[0].toLocalFile()
            if os.path.isdir(path):
                self.treeWidget.clearItems()
                self.env.mainWindow.openDirectory(path)
            else:
                self.env.mainWindow.openFile(path, True)

    def mimeTypes(self):
        # This is needed for dropping files in a QTreeWidget
        return ['text/uri-list']
