#!/usr/bin/env python3

#TODO: this script is unfinished

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import re

path = "/boot/syslinux/syslinux.cfg"
configfoo = """PROMPT 0
TIMEOUT 2
UI menu.c32
MENU TITLE Arch Linux
MENU COLOR border       30
MENU COLOR title        1
MENU COLOR sel          7
MENU COLOR unsel        37
MENU COLOR help         37
MENU COLOR timeout_msg  37
MENU COLOR timeout      1
MENU COLOR msg07        37
MENU COLOR tabmsg       31
"""
options = "rw quiet"

class label:
    def __init__(self, labelname, visiblename, vmlinuz, initramfs, rootfs):
        self.labelname = labelname
        self.visiblename = visiblename
        self.vmlinuz = vmlinuz
        self.initramfs = initramfs
        self.rootfs = rootfs

    def labelstring(self):
        return "Label " + self.labelname + """
    MENU LABEL """ + self.visiblename + """
    LINUX """ + self.vmlinuz + """
    APPEND root="""+ self.rootfs + " " + options + """
    INITRD """ + self.initramfs


def parselabels():

    l = []
    with open(path, "r") as f:
        state = None
        labelname = ""
        visiblename = ""
        vmlinuz = ""
        initramfs = ""
        rootfs = ""
        for i in f:
            if i.strip().startswith("LABEL"):
                state = "LABEL"
                labelname = i.strip().split()[1]
            if state == "LABEL":
                if i.strip().startswith("MENU"):
                    visiblename = i.strip().split()[2]
                if i.strip().startswith("LINUX"):
                    vmlinuz = i.strip().split()[1]
                if i.strip().startswith("APPEND"):
                    rfs = i.strip().split()[2]
                    if rfs.startswith("root=/"): #TODO: UUID, LABEL support
                        rootfs = rfs.split("=")[1]
                if i.strip().startswith("INITRD"):
                    initramfs = i.strip().split()[1]
                    l.append(label(labelname, visiblename, vmlinuz, initramfs, rootfs))
                    state = None
    for i in l:
        print(i.labelstring())
    return l


class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        nameLabel = QLabel("Name:")
        self.nameLine = QLineEdit()
        self.reloadbtn = QPushButton("&(Re)Load config")
        self.reloadbtn.clicked.connect(parselabels)

        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.reloadbtn)

        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Syslinux Configurator")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())