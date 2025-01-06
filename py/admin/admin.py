from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from py.admin.manage_user import UserMange
from py.admin.branch_mange import Branchs,BranchManagerWindow
class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        # إنشاء العنوان
        self.label = QLabel("Admin Control Panel")
        self.label.setAlignment(Qt.AlignCenter)  # محاذاة العنوان في المنتصف
        self.label.setFont(QFont("Arial", 20))  # تعيين خط أكبر للعنوين
        self.label.setMaximumHeight(50)
        self.layout.addWidget(self.label)
        self.create_buttons()

    def user_mangeuser(self):

        self.user_management = UserMange()
        self.user_management.setWindowModality(Qt.ApplicationModal)  # جعلها نافذة حوارية
        self.user_management.show()

    def branch_mange(self):
    # استدعاء نافذة UserMange عند الضغط على الزر
        self.branch_mange_window = Branchs()  # إنشاء كائن من UserMange
        self.branch_mange_window .setWindowModality(Qt.ApplicationModal)  # جعلها نافذة حوارية
        self.branch_mange_window.show()  # عرض نافذة إدارة المستخدمين

    def branches_manger(self):
    # استدعاء نافذة UserMange عند الضغط على الزر
        self.branch_mangeuser_window = BranchManagerWindow()  # إنشاء كائن من UserMange
        self.branch_mangeuser_window.setWindowModality(Qt.ApplicationModal)  # جعلها نافذة حوارية 
        self.branch_mangeuser_window.show()  # عرض نافذة إدارة المستخدمين

    def create_buttons(self):
        button_layout = QHBoxLayout()

        self.user_manger = QPushButton("Users Manager")
        self.user_manger.clicked.connect(self.user_mangeuser)  # ربط الزر بالوظيفة
        button_layout.addWidget(self.user_manger)

        # إنشاء الزر الخاص بإدارة الفروع
        self.Branches= QPushButton("Branches")
        self.Branches.clicked.connect(self.branch_mange)  # ربط الزر بالوظيفة
        button_layout.addWidget(self.Branches)
       
        # إنشاء الزر الخاص بإدارة الفروع
        self.Branches_manger = QPushButton("Branches Manager")
        self.Branches_manger.clicked.connect(self.branches_manger)  # ربط الزر بالوظيفة
        button_layout.addWidget(self.Branches_manger)
       
       
        # إضافة الزر إلى التخطيط الرئيسي
        self.layout.addLayout(button_layout)

        # تعيين التخطيط النهائي للنافذة
        self.setLayout(self.layout)