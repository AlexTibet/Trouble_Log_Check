from player import Player

from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from UI_tlc_gui import Ui_MainWindow
import sys
import check_functions as cf
from download_log_file import download_log

file_name = 'None'
hello = '\t\tПриветствую!\n\n\tПрограмма Trouble Log Check\n\tразработана специально для сервера TROUBLE HOME\n'\
          '\tВ игре Beasts Of Bermuda\n\n\tНапоминаю что .log файлы часто очень большие\n\tПроявите терпение если' \
          ' скачиваете\n\n\tВ ЭТОЙ ВЕРСИИ МОЖНО ПОСМОТРЕТЬ ТОЛЬКО "ВСЁ" И "ПО SteamID"'

# Create application
app = QApplication()

# Create form and init UI
Form = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(Form)
Form.show()

# Hook Logic


def pb_download():
    global file_name
    if ui.checkBox.isChecked():
        file_name = download_log(True, False)
    if ui.checkBox_2.isChecked():
        file_name = download_log(False, True)
    ui.lineEdit_for_log_file.setText(file_name)
    ui.textEdit.clear()
    ui.textEdit.insertPlainText('\n\n\nФайл загружен')


def pb_ok_with_stid():
    steam_id = ui.lineEdit_SteamID.text()
    if len(steam_id) < 5:
        ui.textEdit.clear()
        ui.textEdit.insertPlainText('Нужно ввести SteamID')
    else:
        ui.textEdit.clear()
        try:
            ui.textEdit.insertPlainText(cf.check_all_player(file_name, steam_id))
        except FileNotFoundError:
            ui.textEdit.insertPlainText('Файл не выбран')


def pb_find_log_file():
    global file_name
    file_name = QFileDialog.getOpenFileName()[0]
    ui.lineEdit_for_log_file.setText(file_name)


def pb_check_death():
    ui.textEdit.clear()
    try:
        ui.textEdit.insertPlainText(cf.check_all_death(file_name))
    except FileNotFoundError:
        ui.textEdit.insertPlainText('Файл не выбран')


def pb_check_global_chat():
    ui.textEdit.clear()
    try:
        ui.textEdit.insertPlainText(cf.check_global_chat(file_name))
    except FileNotFoundError:
        ui.textEdit.insertPlainText('Файл не выбран')


def pb_check_all_chat():
    ui.textEdit.clear()
    try:
        ui.textEdit.insertPlainText(cf.check_all_chat(file_name))
    except FileNotFoundError:
        ui.textEdit.insertPlainText('Файл не выбран')


def pb_check_all():
    ui.textEdit.clear()
    try:
        ui.textEdit.insertPlainText(cf.check_all_player(file_name, None))
    except FileNotFoundError:
        ui.textEdit.insertPlainText('Файл не выбран')


if __name__ == '__main__':
    ui.textEdit.insertPlainText(hello)
    ui.Button_with_download_log_file.clicked.connect(pb_download)
    ui.toolButton_forlog_file.clicked.connect(pb_find_log_file)
    ui.Button_with_chek_SteamId.clicked.connect(pb_ok_with_stid)
    ui.pushButton_for_all_death.clicked.connect(pb_check_death)
    ui.pushButton_for_global_chat.clicked.connect(pb_check_global_chat)
    ui.pushButton_all_chat.clicked.connect(pb_check_all_chat)
    ui.pushButton_all_lpg.clicked.connect(pb_check_all)

    sys.exit(app.exec_())
