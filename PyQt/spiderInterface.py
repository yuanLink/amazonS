#   -*- coding:utf-8 -*-

__author__ = "Link"

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import ui_Dialog
import sys,os
sys.path.append('..')
from spider import amazonSpider
import threading


class SpiderDialog(QDialog, ui_Dialog.Ui_Dialog):
    """docstring for SpiderDialog"""
    def __init__(self, parent=None):
        super(SpiderDialog, self).__init__(parent)
        self.setupUi(self)
        self.takeButton.setFocusPolicy(Qt.NoFocus)
        self.result = None
        self.updateUi()

    @pyqtSlot(bool)
    def spiderFinish(self, result):
        """ the spider is finish"""
        print("There!")
        if result == True:
            self.KeywordText.setText("爬虫已经完成任务")
        else:
            self.KeywordText.setText("你的url有问题...")

        self.takeButton.setEnabled(True)

    def updateUi(self):
        # print("int update")
        enable = (not self.UrlText.toPlainText() == '' ) and (not 
            self.KeywordText.toPlainText() == '')
        self.takeButton.setEnabled(enable)


    def submitRequest(self):
        """ to submit this request to get picture and excel
        """
        url = self.UrlText.toPlainText()
        keywords = self.KeywordText.toPlainText()
        self.UrlText.setText("正在写入数据...请稍后")
        self.KeywordText.setText("正在写入数据...请稍后")
        self.Spider = SpiderCrawl({keywords:url}, self)
        # self.connect(self.Spider, SIGNAL("SignalFinishSpdier"), self, SLOT("spiderFinish"))
        self.Spider.start()
        self.takeButton.setEnabled(False)
        # result = amazonSpider.Spider({keywords:url})

class SpiderCrawl(QThread):
    """Lanch Spider"""
    SignalFinishSpdier = pyqtSignal(bool)
    def __init__(self, needs, parent=None):
        super(SpiderCrawl, self).__init__(parent)
        self.needs = needs
        self.SignalFinishSpdier.connect(parent.spiderFinish)

    def run(self):
        """ it will return result of the spider
        
        Ret: the result of spider
        """
        result = amazonSpider.Spider(self.needs)
        self.SignalFinishSpdier.emit(result)
        
if __name__ == "__main__":

    app = QApplication(sys.argv)
    myshow = SpiderDialog()
    myshow.show()
    sys.exit(app.exec_())