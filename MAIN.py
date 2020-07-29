import sys, os, json
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import*
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWebEngine
from PyQt5.QtWebEngine import*
class Adressb(QLineEdit):
    def __init__(self):
        super().__init__()

        def mousePressEvent(self, e):
            self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A_browser")
        self.createapp()
        self.setWindowIcon(QIcon("A.jpg"))
        self.setMinimumSize(1000, 500)

    def createapp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # create tab
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)

        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.tabbar.setLayoutDirection(Qt.LeftToRight)
        self.tabbar.setElideMode(Qt.ElideLeft)
        self.shortcutNewTab = QShortcut(QKeySequence("ctrl+n"), self)
        self.shortcutNewTab.activated.connect(self.AddTab)
        self.shortcutreload = QShortcut(QKeySequence("F5"), self)
        self.shortcutreload.activated.connect(self.reloadp)

        #KEEP TRACK
        self.tabCount =0
        self.tabs=[]


        # create addressbar
        self.Toolbar = QWidget()
        self.Toolbarlayout = QHBoxLayout()
        self.adressbar = Adressb()
        self.AddtTabButton = QPushButton("+")

        self.adressbar.returnPressed.connect(self.BrowseTo)
        self.AddtTabButton.clicked.connect(self.AddTab)

        #set toolbar button
        self.Backbutton=QPushButton("<-")
        self.Backbutton.clicked.connect(self.Goback)

        self.forwardbtn=QPushButton("->")
        self.forwardbtn.clicked.connect(self.Gofront)

        self.reloadbtn=QPushButton("r")
        self.reloadbtn.clicked.connect(self.reloadp)

        #toolbar
        self.Toolbar.setLayout(self.Toolbarlayout)
        self.Toolbarlayout.addWidget(self.Backbutton)
        self.Toolbarlayout.addWidget(self.forwardbtn)
        self.Toolbarlayout.addWidget(self.adressbar)
        self.Toolbarlayout.addWidget(self.reloadbtn)
        # new tab

        self.Toolbarlayout.addWidget(self.AddtTabButton)

        # SET MAIN VIEW
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)

        self.AddTab()

        self.show()

    def CloseTab(self, i):
        self.tabbar.removeTab(i)

    def AddTab(self):
            i=self.tabCount

            self.tabs.append(QWidget())
            self.tabs[i].layout= QVBoxLayout()
            self.tabs[i].layout.setContentsMargins(0,0,0,0 )

            self.tabs[i].setObjectName("Tab" + str(i))

            #open web view
            self.tabs[i].content=QWebEngineView()
            self.tabs[i].content.load(QUrl.fromUserInput("http://google.com"))

            self.tabs[i].content.titleChanged.connect(lambda :self.setTabContent(i,"title"))
            self.tabs[i].content.iconChanged.connect(lambda : self.setTabContent(i,"icon"))
            self.tabs[i].content.urlChanged.connect(lambda : self.setTabContent(i,"url"))

            self.tabs[i].splitview = QSplitter()
            self.tabs[i].splitview.setOrientation(Qt.Vertical)
            self.tabs[i].layout.addWidget(self.tabs[i].splitview)
            self.tabs[i].splitview.addWidget(self.tabs[i].content)

#            self.tabs[i].layout.addWidget(self.tabs[i].content)

            self.tabs[i].setLayout(self.tabs[i].layout)

            self.container.layout.addWidget(self.tabs[i])
            self.container.layout.setCurrentWidget(self.tabs[i])

            self.tabbar.addTab("newtab")
            self.tabbar.setTabData(i, {"object":"Tab"+ str(i),"initial":i})
            self.tabbar.setCurrentIndex(i)

            self.tabCount+=1

    def SwitchTab(self,i):
        if self.tabbar.tabData(i):
            td=self.tabbar.tabData(i)["object"]
            print("tab:",td)
            tc=self.findChild(QWidget,td)
            self.container.layout.setCurrentWidget(tc)
            newurl=tc.content.url().toString()
            self.adressbar.setText(newurl)

    def BrowseTo(self):
        text= self.adressbar.text()
        print(text)

        i=self.tabbar.currentIndex()
        tab= self.tabbar.tabData(i)["object"]
        wv= self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url="http://www.google.com/search?q=" + text
            else:
                url="http://" +text
        else:
            url=text

        wv.load(QUrl.fromUserInput(url))

    def setTabContent(self, i,type):
        '''
                        self.tabs[i].objectName=tab1
                        self.tabbar.tabData(i)["object]=tab1
        '''
        tab_Name = self.tabs[i].objectName()
        # tab1

        count = 0
        running = True

        currenttab=self.tabbar.tabData(self.tabbar.currentIndex())["object"]

        if currenttab== tab_Name and type=="url":
            newurl=self.findChild(QWidget,tab_Name).content.url().toString()
            self.adressbar.setText(newurl)
            return False
        while running:
            tabdataname = self.tabbar.tabData(count)
            if count > 99:
                running = False
            if tab_Name == tabdataname["object"]:
                if type=="title":
                    newTitle = self.findChild(QWidget, tab_Name).content.title()
                    self.tabbar.setTabText(count, newTitle)
                elif type=="icon":
                   newIcon=self.findChild(QWidget, tab_Name).content.icon()
                   self.tabbar.setTabIcon(count, newIcon)

                running = False
            else:
                count += 1

    def Goback( self):
        activeIndex = self.tabbar.currentIndex()
        tab_name=self.tabbar.tabData(activeIndex)["object"]
        tab_content=self.findChild(QWidget, tab_name).content

        tab_content.back()
    def   Gofront(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.forward()

    def reloadp(self):
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.reload()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "667"

    with open("material.css","r") as style:
        app.setStyleSheet(style.read())
    sys.exit(app.exec_())
