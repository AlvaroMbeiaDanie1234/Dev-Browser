import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # create a status bar at the bottom
        self.statusBar()

        # create a progress bar and add it to the status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        self.progress_bar.setMaximumHeight(12)
        self.statusBar().addPermanentWidget(self.progress_bar)

        # hide the progress bar by default
        self.progress_bar.setVisible(False)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        style = '''
        QWebEngineView {
        border: 1px solid gray;
        border-radius: 10px;
        color: #001721;
        }
        '''
        self.browser.setStyleSheet(style)

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon('assets/back.png'), 'Voltar', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon('assets/front.png'), 'Avançar', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar = self.addToolBar('Navigation')
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon('assets/update.png'),   'Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon('assets/home.png'),   'Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        view_source_btn = QAction(QIcon('assets/code.png'), 'View Page Source', self)
        view_source_btn.triggered.connect(self.view_page_source)
        navbar.addAction(view_source_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        style_sheet = """
        QLineEdit {
            border: 2px solid #ccc;
            border-radius: 15px;
            padding: 5px;
            background: #f0f0f0;
            selection-background-color: darkgray;
        }
        QLineEdit:focus {
            border: 2px solid #555;
            background: #fff;
        }
        """
        self.url_bar.setStyleSheet(style_sheet)

        # connect signals for loading progress and url changes
        self.browser.loadStarted.connect(self.show_progress)
        self.browser.loadFinished.connect(self.hide_progress)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def show_progress(self):
        self.progress_bar.setVisible(True)

    def hide_progress(self):
        self.progress_bar.setVisible(False)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def view_page_source(self):
        self.browser.page().toHtml(lambda html: self.show_page_source(html))

    def show_page_source(self, html):
        dialog = QDialog(self)
        dialog.setWindowTitle('Page Source')
        dialog.resize(800, 600)

        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit(dialog)
        text_edit.setPlainText(html)
        layout.addWidget(text_edit)
        text_edit.textChanged.connect(lambda: self.update_page_content(text_edit.toPlainText()))
        dialog.exec_()

    def update_page_content(self, new_html):
        page = self.browser.page()
        page.setContent(new_html.encode())

app = QApplication(sys.argv)
QApplication.setApplicationName('DEV | Browser')
window = MainWindow()
app.exec_()