import sys

from JobCrawler.crawler import Crawler
import JobCrawler.db as job_db

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from UI.Ui_job_crawler_app import Ui_Form
from UI.Ui_job_table_view import Ui_Form as table_view

BASE_URL = 'https://www.jobs.bg/front_job_search.php?subm=1&keywords%5B%5D=python'

class MainWindow(qtw.QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Ui_Form.__init__(self)

        self.setupUi(self)
        self.setWindowTitle('Job Crawler')

        # btn_read_new_data = qtw.QPushButton('Read new data')
        # btn_read_new_data.setGeometry(100,50,50,50)
        # btn_view_table = qtw.QPushButton('View table')
        # self.setGeometry(1000, 200, 200, 60)
        #
        # # create main layout
        # main_layout = qtw.QVBoxLayout(self)
        # main_layout.addWidget(btn_read_new_data)
        # main_layout.addWidget(btn_view_table)
        #
        self.Btn_read_site.clicked.connect(self.onBtnReadNewDataClick)
        self.Btn_load_all.clicked.connect(self.onBtnViewTableClick)
        self.Btn_close.clicked.connect(self.onBtnCloseClick)

        self.show()

    @qtc.pyqtSlot(bool)
    def onBtnReadNewDataClick(self, *args):
        job_cr = Crawler(BASE_URL)
        job_cr.start()
        list_job = job_cr.jobs
        print(len(list_job))

        # if it crawls the site from scratch - first clear DB
        db = job_db.DB()
        db.drop_jobadv_table()
        db.create_jobadv_table()

        # db.get_info_in_db()
        db.insert_jobs(list_job)
        job_cr.close()


    @qtc.pyqtSlot(bool)
    def onBtnViewTableClick(self, *args):
        form_table_view = table_view()


    @qtc.pyqtSlot(bool)
    def onBtnCloseClick(self, *args):
        self.close()


if __name__=='__main__':
    app = qtw.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())
