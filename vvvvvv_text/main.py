#!/usr/bin/env python3
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QPushButton, QLabel, QPlainTextEdit, QSizePolicy, QComboBox, QStackedLayout, QDialog, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont, QColor, QFontDatabase, QImage, QClipboard
from PyQt5.QtCore import Qt, QRect, QPoint
import sys
import textwrap
import math
import os

colors = [
    (164,164,255),
    (255,60,60),
    (144,255,144),
    (95,95,255),
    (255,134,255),
    (229,229,120),
    (174,174,174),
    (19,174,174),
    (19,60,60),
    (19,255,144),
    (19,255,134),
    (19,95,255),
    (19,134,255),
    (19,164,255)
]

color_names = ["Cyan", "Red", "Green", "Blue", "Purple", "Yellow", "Gray", "Teal", "Dark Teal", "Spring Green", "Darker Spring Green", "Bright Blue", "Brighter Blue", "Aqua"]

squeaks = ["None", "Cyan", "Red", "Green", "Blue", "Purple", "Yellow", "Terminal"]

crewmate_positions = ["Player", "Cyan", "Red", "Green", "Blue", "Purple", "Yellow"]

font_spacestation = QFont('Space Station VCE', 12)
font_spacestation.setStyleStrategy(QFont.NoAntialias)


def GetRealColorName(index):
    translation = [0,1,2,3,4,5,6,6,1,2,5,3,4,0]
    return color_names[translation[index]]

def PaintTextbox(painter,x,y,text,color):
    painter.setFont(font_spacestation)
    lines = []
    for line in text.split("\n"):
        lines.append("\n".join(textwrap.wrap(line, width=36, drop_whitespace=True)))
    text = "\n".join(lines)
        
    text_width = 0
    for line in text.split("\n"):
        if (len(line) * 16) > text_width:
            text_width = len(line) * 16

    text_height = len(text.split("\n")) * 16
        
    painter.setPen(QPen(QColor(color[0] / 6, color[1] / 6, color[2] / 6), 1, Qt.SolidLine))
    painter.setBrush(QBrush(QColor(*color), Qt.SolidPattern))
    painter.drawRect(QRect(QPoint(x + 0, y + 0), QPoint(x + 24 + text_width + 6,y + 24 + text_height + 6)))
    painter.drawRect(QRect(QPoint(x + 1, y + 1), QPoint(x + 23 + text_width + 6,y + 23 + text_height + 6)))

    painter.drawRect(QRect(QPoint(x + 6, y + 6), QPoint(x + 18 + text_width + 6,y + 18 + text_height + 6)))
    painter.drawRect(QRect(QPoint(x + 7, y + 7), QPoint(x + 17 + text_width + 6,y + 17 + text_height + 6)))
        
    painter.setPen(QPen(QColor(color[0] / 6, color[1] / 6, color[2] / 6), 1, Qt.SolidLine))
    painter.setBrush(QBrush(QColor(color[0] / 6, color[1] / 6, color[2] / 6), Qt.SolidPattern))
        

    painter.drawRect(QRect(QPoint(x + 10, y + 10), QPoint(x + 14 + text_width + 6, y + 14 + text_height + 6)))
        
    painter.setPen(QColor(*color))
    for index, line in enumerate(text.split("\n")):
        painter.drawText(x + 16, y + 32 + (index * 16) - 2, line)
    return (text_width, text_height)


class TextboxWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = (164,164,255)
        
        self.text = ""
        self.width = 320
        self.height = 48
        
        self.minimumHeight = 100


    def sizeHint(self):
        return QtCore.QSize(self.width,self.height)

    def minimumSizeHint(self):
        return QtCore.QSize(self.width,self.height)
        
    def paintEvent(self, e):

        painter = QPainter(self)
        
        text_width, text_height = PaintTextbox(painter,0,0,self.text,self.color)
        
        self.width = text_width + 32
        self.height = text_height + 32
        self.resize(self.width, self.height)
        self.updateGeometry()
        
        painter.end()
        
    def text_updated(self,text):
        self.text = text
        self.update()

    def change_color(self, ind):
        self.color = colors[ind]
        self.update()

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Textbox Generator"

        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/space_station.ttf")
        
        self.textbox_position_x = 20
        self.textbox_position_y = 20
        self.textbox_position_type = 0
        self.textbox_color = 0
        self.textbox_text = ""
        
        self.textbox_squeak = 0
        self.textbox_position_crewmate = 0
        
        
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(__file__) + "/icon.png"))
        self.setWindowTitle(self.title)

        self.resize(640,480)

        self.layout = QGridLayout()

        self.widget_textbox = TextboxWidget()
        self.widget_text_input_label = QLabel('Text:')
        self.widget_text_input = QPlainTextEdit()

        self.widget_save_image = QPushButton("Save image")
        self.widget_copy_image = QPushButton("Copy image to clipboard")

        self.widget_color_label = QLabel('Color:')
        self.widget_color = QComboBox()
        self.widget_color.addItems(color_names)

        self.widget_position_label = QLabel('Position:')
        self.widget_position = QComboBox()
        self.widget_position.addItems(["Centered", "Horizontally centered", "Vertically centered", "Above...", "Below...", "Absolute"])
        self.widget_position_above = QComboBox()
        self.widget_position_above.addItems(crewmate_positions)
        self.widget_position_edit = QPushButton("Place textbox")

        self.widget_squeak_label = QLabel('Squeak:')
        self.widget_squeak = QComboBox()
        self.widget_squeak.addItems(squeaks)

        self.widget_text_output_label = QLabel('Generated script:')
        self.widget_text_output = QPlainTextEdit()

        self.widget_text_input.textChanged.connect(self.text_updated)
        self.widget_text_input.resize(165, self.widget_text_input.height());

        self.widget_color.currentIndexChanged.connect(self.change_color)

        self.widget_squeak.currentIndexChanged.connect(self.change_squeak)

        self.layout.addWidget(self.widget_textbox,0,0,1,0)
        self.layout.addWidget(self.widget_save_image,1,0)
        self.layout.addWidget(self.widget_copy_image,1,1)
        self.layout.addWidget(self.widget_text_input_label,2,0)
        self.layout.addWidget(self.widget_text_input,3,0,1,0)
        self.layout.addWidget(self.widget_color_label,4,0)
        self.layout.addWidget(self.widget_color,4,1)
        self.layout.addWidget(self.widget_position_label,5,0)
        self.layout.addWidget(self.widget_position,5,1)
        self.layout.addWidget(self.widget_position_above,5,2)
        self.layout.addWidget(self.widget_position_edit,5,3)
        self.layout.addWidget(self.widget_squeak_label,6,0)
        self.layout.addWidget(self.widget_squeak,6,1)
        self.layout.addWidget(self.widget_text_output_label,7,0)
        self.layout.addWidget(self.widget_text_output,7,1)
        
        self.widget_position_above.setEnabled(False)
        self.widget_position_edit.setEnabled(False)
        self.widget_save_image.clicked.connect(self.save_image)
        self.widget_copy_image.clicked.connect(self.copy_image)
        self.widget_position_edit.clicked.connect(self.edit_position)
        self.widget_position.currentIndexChanged.connect(self.change_buttons)
        self.widget_position_above.currentIndexChanged.connect(self.change_position_above)
        
        self.update_script()
        
        self.layout.setColumnStretch(1,1)
        self.setLayout(self.layout)
        self.show()

    def text_updated(self):
        self.textbox_text = self.widget_text_input.toPlainText()
        self.widget_textbox.text_updated(self.textbox_text)
        self.update_script()
        
    def change_color(self, ind):
        self.widget_textbox.change_color(ind)
        self.textbox_color = ind
        self.update_script()
    
    def change_squeak(self, ind):
        self.textbox_squeak = ind
        self.update_script()
        
    def edit_position(self):
        self.window = PositionWindow(self)
        self.window.setWindowModality(Qt.ApplicationModal)
        self.window.exec_()

        self.textbox_position_x = self.window.textbox_x
        self.textbox_position_y = self.window.textbox_y
        self.update_script()

    def save_image(self):
    
        fname = QFileDialog.getSaveFileName(self, 'Save image', './',"PNG (*.png);;JPEG (*.jpg; *.jpeg);;BMP (*.bmp);;TIFF (*.tiff; *.tif);;GIF (*.gif);;WEBP (*.webp)")
        if not fname[0]:
            return

        image = QImage(2000, 2000, QImage.Format_RGB32)
        painter = QtGui.QPainter(image)
        text_width, text_height = PaintTextbox(painter,0,0,self.textbox_text,colors[self.textbox_color])
        painter.end()
        width = text_width + 32
        height = text_height + 32
        
        image2 = image.copy(0,0,width,height)
        image2.save(fname[0])
        
        pass
    
    def copy_image(self):
        image = QImage(2000, 2000, QImage.Format_RGB32)
        painter = QtGui.QPainter(image)
        text_width, text_height = PaintTextbox(painter,0,0,self.textbox_text,colors[self.textbox_color])
        painter.end()
        width = text_width + 32
        height = text_height + 32
        
        image2 = image.copy(0,0,width,height)
        QApplication.clipboard().setImage(image2)
    
    def change_buttons(self, index):
        self.textbox_position_type = index
        self.widget_position_above.setEnabled(False)
        self.widget_position_edit.setEnabled(False)
        if index in [1, 2, 5]:
            self.widget_position_edit.setEnabled(True)
        if index in [3, 4]:
            self.widget_position_above.setEnabled(True)
        self.update_script()

    def change_position_above(self, index):
        self.textbox_position_crewmate = index
        self.update_script()
    
    def update_script(self):
    
        lines = []
        for line in self.textbox_text.split("\n"):
            lines.append("\n".join(textwrap.wrap(line, width=36, drop_whitespace=False)))
        text = "\n".join(lines)
    
    
        script = ""
        if self.textbox_squeak != 0:
            script += "squeak(" + squeaks[self.textbox_squeak].lower() + ")\n"
        script += "text("
        script += GetRealColorName(self.textbox_color).lower() + ","
        script += str(self.textbox_position_x) + "," + str(self.textbox_position_y) + "," + str(len(text.split("\n"))) + ")\n"
        script += text + "\n"
        if self.textbox_color > 6:
            script += "createcrewman(-20,0,gray,0,faceleft)\n"
        if self.textbox_position_type != 5:
            script += "position("
            translation = ["center", "centerx", "centery", "above", "below"]
            if self.textbox_position_type in range(0,3):
                script += translation[self.textbox_position_type]
            else:
                script += crewmate_positions[self.textbox_position_crewmate].lower()
                script += ","
                script += translation[self.textbox_position_type]
            script += ")\n"
        script += "speak_active\n"
        script += "endtext"
        
        self.widget_text_output.setPlainText(script)


class PositionWindow(QDialog):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.title = "Position Textbox"
        self.textbox_x = parent.textbox_position_x
        self.textbox_y = parent.textbox_position_y
        self.textbox_position_type = parent.textbox_position_type
        self.textbox_width = 0
        self.textbox_height = 0
        
        self.textbox_color = parent.textbox_color
        self.textbox_text = parent.textbox_text
        
        self.offset_x = 0
        self.offset_y = 0
        self.mouse_down = False

        QFontDatabase.addApplicationFont(os.path.dirname(__file__) + "/space_station.ttf")
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(__file__) + "/icon.png"))
        self.setWindowTitle(self.title)

        self.resize(640,480)

        self.setMouseTracking(True)
        self.setFocus()
        self.setStyleSheet("background-color: black;")
    def paintEvent(self, e):
        painter = QPainter(self)

        text_width, text_height = PaintTextbox(painter,self.textbox_x,self.textbox_y,self.textbox_text,colors[self.textbox_color])
        self.textbox_width = text_width + 32
        self.textbox_height = text_height + 32

        painter.setPen(QColor(0,0,0))
        painter.drawText(8,  10 + 16, "[Press ENTER to return to editor]")
        painter.drawText(12, 10 + 16, "[Press ENTER to return to editor]")
        painter.drawText(10, 8  + 16, "[Press ENTER to return to editor]")
        painter.drawText(10, 12 + 16, "[Press ENTER to return to editor]")
        painter.setPen(QColor(196,196,250))
        painter.drawText(10, 10 + 16, "[Press ENTER to return to editor]")
        
        painter.end()

    def mouseMoveEvent(self, e):
        if self.mouse_down:
            self.textbox_x = self.offset_x + e.x()
            self.textbox_y = self.offset_y + e.y()
            self.textbox_x = math.floor(self.textbox_x / 2) * 2
            self.textbox_y = math.floor(self.textbox_y / 2) * 2

            if self.textbox_x < 20:
                self.textbox_x = 20
            if self.textbox_y < 20:
                self.textbox_y = 20
            if self.textbox_x + self.textbox_width >= 620:
                self.textbox_x = 620 - self.textbox_width
            if self.textbox_y + self.textbox_height >= 460:
                self.textbox_y = 460 - self.textbox_height
            
            if self.textbox_position_type == 1:
                self.textbox_x = 320 - self.textbox_width / 2
            if self.textbox_position_type == 2:
                self.textbox_y = 240 - self.textbox_height / 2
            self.update()
        
    def mousePressEvent(self, e):
        self.offset_x = self.textbox_x - e.x()
        self.offset_y = self.textbox_y - e.y()
        self.mouse_down = True

    def mouseReleaseEvent(self, e):
        self.mouse_down = False
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.close()


def run():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    run()