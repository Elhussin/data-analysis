import sys
from PyQt5.QtWidgets import QApplication, QDialog
from py.mainWindow import MainWindow
from PyQt5.QtCore import QTimer
import os
from py.layOut.icon import IconManager ,set_default_title
from py.functian import load_stylesheet
from py.auth.login import LoginDialog


if __name__ == "__main__":
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # استخدام هذه الطريقة للوصول إلى ملفات QSS والصور
    qss_path = resource_path("py/static/style/auth.qss")
    icon_path = resource_path("py/static/media/icon.ico")

    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    login_dialog.show()

    app.setStyle("Fusion")  # تعيين نمط واجهة موحد

    

    load_stylesheet(app, qss_path)

    app.focusChanged.connect(lambda: set_default_title("Orders"))

    # icon_path = "py/static/media/icon.ico"  # ضع مسار أيقونتك هنا
    icon_manager = IconManager(app, icon_path, app_name="Orders")

    if login_dialog.exec_() == QDialog.Accepted:
        
        window = MainWindow()
        window.resize(800, 600)
        window.show()  # إظهار النافذة
        # self.init_ui() #تهيئة واجهة المستخدم الرئيسية
    else:
        sys.exit()
    sys.exit(app.exec_())
