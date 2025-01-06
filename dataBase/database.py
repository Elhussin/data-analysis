import sqlite3
from dataBase.encrypet import EncryptionManager
from py.functian import result_as_dict
from dataBase.DatabaseManager import DatabaseManager,table_definitions

import sys
import os

class UserDatabase:
    def __init__(self):
        self.db_path =  os.path.join(os.path.dirname(__file__), 'shop.db')
        print(self.db_path)
                # إنشاء الملف إذا لم يكن موجودًا
        if not os.path.exists(self.db_path):
            open(self.db_path, 'w').close()  # إنشاء ملف فارغ

        db_manager = DatabaseManager(self.db_path)
        db_manager.create_all_tables(table_definitions)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # self.encryption_manager = EncryptionManager() # تشفير كلمة المرور
    
    def add_user(self,username, password, full_name, email):
        """ إضافة مستخدم جديد إلى قاعدة البيانات """
        # encrypted_password = self.encryption_manager.encrypt_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username, password,full_name,email) VALUES (?,?,?,?)", (username, password,full_name, email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # إذا كان اسم المستخدم موجودًا بالفعل


    def add_user_by_admin(self,username,full_name,email,status,user_type, password):
        """ إضافة مستخدم جديد إلى قاعدة البيانات """
        # encrypted_password = self.encryption_manager.encrypt_password(password)
        try:
            self.cursor.execute("INSERT INTO users (username, password,full_name,email,status,user_type) VALUES (?,?,?,?,?,?)", (username, password,full_name, email,status,user_type))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # إذا كان اسم المستخدم موجودًا بالفعل

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = self.cursor.fetchone()
        description=self.cursor.description

        user=result_as_dict(user_data,description)
        if user:
            return user
        return None

    def update_user(self, user_id, username, full_name, email, status, user_type, password):
        # encrypted_password = self.encryption_manager.encrypt_password(password)
        """تحديث بيانات فرع معين"""
        query = '''
        UPDATE users 
        SET username = ?, full_name = ?, email = ?, status = ?,user_type=?,password=?,last_update = CURRENT_TIMESTAMP
        WHERE id = ?;
        '''

        # user_id, username, full_name, email, status, user_type, password
        self.cursor.execute(query, ( username, full_name, email, status, user_type, password,user_id,))
        self.conn.commit()

    def update_user_without_password(self, user_id, username, full_name, email, status, user_type):
        query = """
        UPDATE users
        SET username = ?, full_name = ?, email = ?, status = ?, user_type = ?,last_update = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        self.cursor.execute(query, (username, full_name, email, status, user_type, user_id))
        self.conn.commit()

    def check_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = self.cursor.fetchone()
        description=self.cursor.description

        user=result_as_dict(user_data,description)
        if user:
            # decrypted_password = self.encryption_manager.decrypt_password(user['password'])
            # return user if decrypted_password == password else None
            return user if user['password'] == password else None
        return None
    
    def get_all_users(self):
        """ استرجاع جميع المستخدمين """
        self.cursor.execute("SELECT * FROM users")
        user_data= self.cursor.fetchall()
        description=self.cursor.description

        users=result_as_dict(user_data,description)
        if users:
            return users 
        return None

               # الحصول على أسماء الأعمدة من cursor.description
    


    def delete_user(self, user_id):
        """ حذف مستخدم من قاعدة البيانات """
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def load_data(self):
        self.cursor.execute('SELECT * FROM Orders')
        return self.cursor.fetchall()

    def insert_data(self, data):
        self.cursor.execute('INSERT INTO Orders (data) VALUES (?)', (data,))
        self.conn.commit()
   
    def close(self):
        self.conn.close()



  
    def create_user_session(self, user_id):
        """ إنشاء جلسة جديدة عند تسجيل الدخول """
        self.cursor.execute('''
            INSERT INTO sessions (user_id, is_active)
            VALUES (?, ?)
        ''', (user_id, True))
        self.conn.commit()

    def get_active_session(self, user_id):
        """ استرجاع الجلسة النشطة للمستخدم """
        self.cursor.execute('''
            SELECT session_id, login_time FROM sessions
            WHERE user_id = ? AND is_active = TRUE
            ORDER BY login_time DESC LIMIT 1
        ''', (user_id,))
        return self.cursor.fetchone()
    

    def dec_active_session(self,user_id):
        """ استرجاع الجلسة النشطة للمستخدم """
        self.cursor.execute('''
            UPDATE sessions SET is_active = FALSE WHERE user_id = ? AND is_active = TRUE
        ''', (user_id,))
        self.conn.commit()

    def fetch_user_name(self, user_id):
        """ استرجاع اسم المستخدم بناءً على الـ ID """
        query = "SELECT username FROM Users WHERE id = ?"
        result = self.cursor.execute(query, (user_id,)).fetchone()  # استخدام fetchone()
        return result[0] if result else None  # إرجاع اسم المستخدم أو None إذا لم يوجد

class BranchDatabase:
    def __init__(self):
        self.db_path =  os.path.join(os.path.dirname(__file__), 'shop.db')
        self.conn = None
        self.cursor = None
        self.connect()


    def connect(self):
        """الاتصال بقاعدة البيانات"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.conn:
            self.conn.close()



    def insert_branch(self, branch_name, branch_location, branch_phone, status):
        """إضافة فرع جديد"""
        try:
            query = '''
            INSERT INTO Branches (branch_name, branch_location, branch_phone, status)
            VALUES (?, ?, ?, ?);
            '''
            self.cursor.execute(query, (branch_name, branch_location, branch_phone, status))
            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False  # إذا كان اسم المستخدم موجودًا بالفعل


    def update_branch(self, branch_id, branch_name, branch_location, branch_phone, status):
        """تحديث بيانات فرع معين"""
        try:
            query = '''
            UPDATE Branches 
            SET branch_name = ?, branch_location = ?, branch_phone = ?, status = ?, last_update = CURRENT_TIMESTAMP
            WHERE id = ?;
            '''
            self.cursor.execute(query, (branch_name, branch_location, branch_phone, status, branch_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


    def delete_branch(self, branch_id):
        """حذف فرع معين"""
        query = 'DELETE FROM Branches WHERE id = ?;'
        self.cursor.execute(query, (branch_id,))
        self.conn.commit()

    def fetch_all_branches(self):
        """إحضار جميع الفروع من قاعدة البيانات"""
        query = 'SELECT * FROM Branches;'
        self.cursor.execute(query)
        branche_data=self.cursor.fetchall()
        description=self.cursor.description

        branche=result_as_dict(branche_data,description)
        if branche:
           return branche
        else:
            return None
        

    def fetch_one_branche(self,branch_id):
        """إحضار فرع  من قاعدة البيانات"""
        
        query = 'SELECT * FROM Branches WHERE id = ?;'
        self.cursor.execute(query, (branch_id,))
        branche_data=self.cursor.fetchone()
        description=self.cursor.description

        branche=result_as_dict(branche_data,description)
        if branche:
           return branche
        else:
            return None
        
    def fetch_branch_name(self, branch_id):
        """ استرجاع اسم الفرع بناءً على الـ ID """
        query = "SELECT branch_name FROM Branches WHERE id = ?"
        result = self.cursor.execute(query, (branch_id,)).fetchone()  # استخدام fetchone()
        return result[0] if result else None  # إرجاع اسم الفرع أو None إذا لم يوجد

    def fetch_branche_by_name(self,branch_name):
        """إحضار فرع  من قاعدة البيانات"""
        
        query = 'SELECT * FROM Branches WHERE branch_name = ?;'
        self.cursor.execute(query, (branch_name,))
        branche_data=self.cursor.fetchone()
        description=self.cursor.description

        branche=result_as_dict(branche_data,description)
        if branche:
            return branche
        else:
            return None
        

class BranchManagerDatabase:

    def __init__(self, ):
        self.db_path =  os.path.join(os.path.dirname(__file__), 'shop.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    def insert_manager(self, branch, user, status, date_end=None):
        """ إضافة سجل جديد في جدول Manager """
        try:
            self.cursor.execute('''
                INSERT INTO Manager (branch, user, status, date_end)
                VALUES (?, ?, ?, ?)
            ''', (branch, user, status, date_end))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    def update_manager(self,branch, user, status, manager_id):
        try:
            """ تعديل سجل Manager """
            self.cursor.execute('''
                UPDATE Manager
                SET branch = ?, user = ?, status = ?,date_end=CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (branch, user, status, manager_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_manager(self, manager_id):
        """ حذف سجل من جدول Manager """
        self.cursor.execute('DELETE FROM Manager WHERE id = ?', (manager_id,))
        self.conn.commit()

    def fetch_all_managers(self):
        """ جلب جميع السجلات من جدول Manager """
        self.cursor.execute('SELECT * FROM Manager')
        all_managers=self.cursor.fetchall()
        description=self.cursor.description

        all_branche_mangers=result_as_dict(all_managers,description)
        if all_branche_mangers:
           return all_branche_mangers
        else:
            return None
        

    def fetch_all_managers_with_details(self):
        """
        جلب جميع السجلات من جدول Manager مع أسماء المستخدمين والفروع
        """
        # الاستعلام باستخدام JOIN
        query = '''
        SELECT 
            Manager.id,
            Manager.user,
            Users.username AS user_name,
            Manager.branch,
            Branches.branch_name AS branch_name,

            Manager.status,
            Manager.date_start,
            Manager.date_end
        FROM 
            Manager
        LEFT JOIN 
            Users ON Manager.user = Users.id
        LEFT JOIN 
            Branches ON Manager.branch = Branches.id;
        '''

        self.cursor.execute(query)
        all_managers = self.cursor.fetchall()
        description = self.cursor.description

        # تحويل النتيجة إلى قائمة من القواميس
        all_branche_managers = result_as_dict(all_managers, description)
        return all_branche_managers if all_branche_managers else None




    def fetch_manager(self, manager_id):
        """ جلب سجل واحد من جدول Manager بناءً على ID """
        self.cursor.execute('SELECT * FROM Manager WHERE id = ?', (manager_id,))
        branche_manger=self.cursor.fetchone()
        description=self.cursor.description

        branche_mangers=result_as_dict(branche_manger,description)
        if branche_mangers:
           return branche_mangers
        else:
            return None

    def fetch_manager_by_user(self, user_id):
        """ جلب سجل واحد من جدول Manager بناءً على ID """
        # تحقق من نوع user_id
        if not isinstance(user_id, (int, str)):
            raise ValueError(f"Invalid type for user_id: {type(user_id)}")

        # تنفيذ الاستعلام
        self.cursor.execute('SELECT * FROM Manager WHERE user = ?', (user_id,))
        branche_manger = self.cursor.fetchone()
        description = self.cursor.description

        # تحويل النتيجة إلى قاموس
        branche_mangers = result_as_dict(branche_manger, description)

        # التحقق من وجود البيانات
        if branche_mangers:
            return branche_mangers
        else:
            return None

    def close(self):
        """إغلاق الاتصال بقاعدة البيانات"""
        if self.conn:
            self.conn.close()

class OrderModel:
    def __init__(self):
        self.db_path =  os.path.join(os.path.dirname(__file__), 'shop.db')
        self.connection = sqlite3.connect(self.db_path)

        self.cursor = self.connection.cursor()
        # db_manager = DatabaseManager(db_path)
        # db_manager.create_all_tables(table_definitions)

    def add_order(self, Serial, branch, user, status="Send To Lab"):
        try:
            self.cursor.execute('''
                INSERT INTO Orders (Serial, branch, user, status)
                VALUES (?, ?, ?, ?)
            ''', (Serial, branch, user, status))
            self.connection.commit()
            return True
        except  sqlite3.IntegrityError:
            return False

    def update_order(self, order_id, **kwargs):
        try:
            columns = ", ".join(f"{key} = ?" for key in kwargs)
            values = list(kwargs.values()) + [order_id]
            self.cursor.execute(f'''
                UPDATE Orders
                SET {columns}
                WHERE id = ?
            ''', values)
            self.connection.commit()
            return True
        except  sqlite3.IntegrityError:
            return False


    def delete_row(self, order_id):
        try:
            self.cursor.execute('DELETE FROM Orders WHERE id = ?', (order_id,))
            self.connection.commit()
            return True
        except  sqlite3.IntegrityError:
            return False
        
   

    def getHeader(self):
            # استعلام للحصول على رؤوس الأعمدة
        self.cursor.execute("PRAGMA table_info('Orders')")
        columns = [row[1] for row in self.cursor.fetchall()]  # العمود الثاني يحتوي على أسماء الأعمدة

        print("Column names:", columns)
        return columns
            # newForm=DynamicForm(self.headers)
         # newForm.show()
    
    def getOrderBySerial(self,order_Serial):
        try:
            self.cursor.execute('SELECT * FROM orders WHERE Serial = ?', (order_Serial,))
            branche_manger=self.cursor.fetchone()
            description=self.cursor.description

            order=result_as_dict(branche_manger,description)
            if order:
                return order
            else:
                return None
        except sqlite3.IntegrityError:
            return None


    def fetch_orders(self,filters=None, search_text=None, status_filter=None, columns=None, limit=None):
        # إذا لم يتم تحديد الأعمدة، يتم استخدام الأعمدة الافتراضية
        if not columns:
            columns = [
                "Orders.id",
                "Orders.Serial",
                "Orders.user || '-' || Users.username AS user",
                "Orders.branch || '-' || Branches.branch_name AS branch",
                "Orders.status",
                "Orders.date_send",
                "Orders.updated_at"
            ]
        
        # تحويل قائمة الأعمدة إلى نص مفصول بفواصل
        selected_columns = ", ".join(columns)
        
        # بناء الاستعلام الأساسي
        query = f"""
            SELECT 
                {selected_columns}
            FROM
                Orders
            LEFT JOIN 
                Users ON Orders.user = Users.id
            LEFT JOIN 
                Branches ON Orders.branch = Branches.id
        """
        values = []
        
        # إضافة شروط التصفية
        conditions = []
        if filters:
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                values.append(value)

        # إضافة شروط البحث
        if search_text:
            conditions.append("(Orders.Serial LIKE ? OR Branches.branch_name LIKE ?)")
            values.extend([f"%{search_text}%", f"%{search_text}%"])
        
        # إضافة شروط الحالة
        if status_filter and status_filter != "All":
            conditions.append("Orders.status = ?")
            values.append(status_filter)
        
        # دمج الشروط معًا
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # إضافة حد للنتائج إذا تم تحديده
        if limit:
            query += f" LIMIT {limit}"
        
        # تنفيذ الاستعلام
        # print(f"Query: {query}")
        # print(f"Values: {values}")
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        description = self.cursor.description

        # تحويل النتائج إلى قاموس
        data_dict = result_as_dict(data, description)

        return data_dict if data_dict else None

    def __del__(self):
        self.connection.close()
    

class PriceList:
    def __init__(self):
        self.db_path =  os.path.join(os.path.dirname(__file__), 'shop.db')
        print("Database path:", self.db_path)

        self.connection = sqlite3.connect(self.db_path)

        self.cursor = self.connection.cursor()

    def fetch_all_data(self, query, params=()):
        """Fetch data from the database based on the provided query."""
        try:
            data=self.cursor.execute(query,params)
            data= self.cursor.fetchall()
            description=self.cursor.description
            dict_data=result_as_dict(data,description)
      
            if dict_data:
           
                return dict_data
                
            else:
                return []
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
        return []

