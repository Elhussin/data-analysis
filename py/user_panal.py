from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from dataBase.database import  UserDatabase
from py.functian import get_credentials_user_id_qsettings



class UserPanal(QWidget):
    def __init__(self):
        super().__init__()
        self.db_users = UserDatabase()
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()

        # إنشاء العنوان
        self.label = QLabel("User Control Panel")
        self.label.setAlignment(Qt.AlignCenter)  # محاذاة العنوان في المنتصف
        self.label.setFont(QFont("Arial", 20))  # تعيين خط أكبر للعناوين
        self.layout.addWidget(self.label)

        # استرجاع بيانات المستخدم
        self.user_id = get_credentials_user_id_qsettings()
        if self.user_id:
            self.userData = self.db_users.get_user_by_id(self.user_id)
            self.display_user_data()
        else:
            self.no_data_label = QLabel("No user data found.")
            self.no_data_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.no_data_label)

        self.setLayout(self.layout)

    def display_user_data(self):
        if self.userData:
            # إنشاء جدول لعرض البيانات
            table = QTableWidget()
            # حساب عدد الصفوف بدون كلمة المرور
            visible_data = {k: v for k, v in self.userData.items() if k != "password"}
            table.setRowCount(len(visible_data))  # عدد الصفوف بناءً على البيانات
            table.setColumnCount(2)  # عمودين: اسم الحقل والقيمة
            table.setHorizontalHeaderLabels(["Field", "Value"])

            # ضبط عرض الأعمدة ليتمدد مع النافذة
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            # تعبئة الجدول بالبيانات
            for i, (key, value) in enumerate(visible_data.items()):
                # تنسيق اسم الحقل: حروف كبيرة واستبدال "_" بمسافة
                formatted_key = key.replace("_", " ").title()

                # إضافة اسم الحقل
                table.setItem(i, 0, QTableWidgetItem(formatted_key))
                # إضافة القيمة
                table.setItem(i, 1, QTableWidgetItem(str(value)))

            self.layout.addWidget(table)
        else:
            self.no_data_label = QLabel("No user data available.")
            self.no_data_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.no_data_label)
