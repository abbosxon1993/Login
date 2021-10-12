import os
import mysql.connector as mysql


class User:
    def __init__(self, name=None, surname=None, login=None, password=None, age=None):
        """Classning asosiy metodi - The main method of the class"""
        self.name = name
        self.surname = surname
        self.login = login
        self.password = password
        self.age = age
        self.numbers = ["1", "2", "3", "4"]
        self.mysql = mysql.connect(host="localhost", user="iqbol", password="qoch12345", database="yangisi")
        self.my_user = self.mysql.cursor()
        self.my_user.execute("create table if not exists username(id int unsigned auto_increment primary key,"
                             "name varchar(20), surname varchar(20), login varchar(20),"
                             "password varchar(20), age int(3))")
        self.old_login_password = []

    @staticmethod
    def show_print():
        """Ekranga chiqaruvchi metod - Display method"""
        print("""
        **>> Welcome to my Homepage <<**

             Registration        [1]
             Login               [2]
             """)

    def selection(self):
        """Raqamlarni tanlash uchun metod - A method for selecting numbers"""
        self.clear()
        self.show_print()

        enter = input("Enter number [1/2]: ").strip()
        while enter not in self.numbers[:2]:
            self.clear()
            print("""
    !!!-> You entered an invalid number <-!!!

             Registration        [1]
             Login               [2]
             """)
            enter = input("Please enter number [1/2]: ").strip()

        if enter == self.numbers[0]:
            self.registration()
        else:
            self.log_in()

    def registration(self):
        """Ro'yhatdan o'tish uchun metod - Method for registration"""
        self.clear()
        print("\n\t\t**>> Registration process <<**\n")
        new_name = input("Enter your name: ").strip().capitalize()
        while not new_name.isalpha():
            self.clear()
            print("\n\t\t**>> Registration process <<**\n")
            print("!!!-> You entered the wrong characters, Please try again <-!!!")
            new_name = input("Enter your name: ").strip().capitalize()

        new_surname = input("Enter your surname: ").strip().capitalize()
        while not new_surname.isalpha():
            self.clear()
            print("\n\t\t**>> Registration process <<**\n")
            print("!!!-> You entered the wrong characters, Please try again <-!!!")
            new_surname = input("Enter your surname: ").strip().capitalize()

        new_login = input("Enter your login: ").strip().lower()
        while not new_login:
            self.clear()
            print("\n\t\t**>> Registration process <<**\n")
            print("!!!-> You entered the wrong characters, Please try again <-!!!")
            new_login = input("Enter your login: ").strip().lower()

        new_password = input("Enter your password: ").strip()
        check_password = input("Check password: ").strip()
        while new_password == "" or new_password != check_password:
            self.clear()
            print("\n\t\t**>> Registration process <<**\n")
            print("!!!-> You entered the wrong characters, Please try again <-!!!")
            new_password = input("Enter your password: ").strip()
            check_password = input("Check password: ").strip()

        new_age = input("Enter your age: ").strip()
        while not new_age.isdigit():
            self.clear()
            print("\n\t\t**>> Registration process <<**\n")
            print("!!!-> You entered the wrong characters, Please try again <-!!!")
            new_age = input("Enter your age: ").strip()

        self.name = new_name
        self.surname = new_surname
        self.login = new_login
        self.password = new_password
        self.age = new_age
        self.write_database()

        self.clear()
        print("""
                            Login change    [1]
                            Password change [2]
                            Log out         [3]
                            Delete account  [4]
                        """)

        enter = input("Enter number [1/2/3/4]: ")
        while enter not in self.numbers:
            self.clear()
            print("""!!!-> You entered the wrong characters <-!!!
                            !!!-> Please try again <-!!!

                            Login change    [1]
                            Password change [2]
                            Log out         [3]
                            Delete account  [4]
                            """)
            enter = input("Enter number [1/2/3/4]: ")

        if enter == self.numbers[0]:
            self.login_change()

        elif enter == self.numbers[1]:
            self.password_change()

        elif enter == self.numbers[2]:
            self.log_out()

        else:
            self.delete_account()

    def write_database(self):
        """Ma'lumotlar bazasiga ma'lumot kiritish uchun metod - A method for entering data into a database"""
        string = f"insert into username(name, surname, login, password, age) values('{self.name}','{self.surname}'," \
                 f"'{self.login}','{self.password}', {self.age})"
        self.my_user.execute(string)
        self.mysql.commit()

    def log_in(self):
        """Tizimga kirish uchun metod - Login method"""
        self.clear()
        print("\n\t\t **>> Login process <<**\n")
        enter_login = input("Enter your login: ").strip().lower()
        enter_password = input("Enter youn password: ").strip()
        while not self.check_login_password(enter_login, enter_password):
            self.clear()
            print("\n\t\t **>> Login process <<**\n")
            print("!!!-> You entered the wrong characters, Please try again <-!!!")
            enter_login = input("Enter your login: ").strip().lower()
            enter_password = input("Enter your password: ").strip()
        self.old_login_password.append(enter_login)
        self.old_login_password.append(enter_password)
        self.clear()
        print("""
                            Login change    [1]
                            Password change [2]
                            Log out         [3]
                            Delete account  [4]
                        """)

        enter = input("Enter number [1/2/3/4]: ")
        while enter not in self.numbers:
            self.clear()
            print("""!!!-> You entered the wrong characters <-!!!
                            !!!-> Please try again <-!!!
                            
                            Login change    [1]
                            Password change [2]
                            Log out         [3]
                            Delete account  [4]
                            """)
            enter = input("Enter number [1/2/3/4]: ")

        if enter == self.numbers[0]:
            self.login_change()

        elif enter == self.numbers[1]:
            self.password_change()

        elif enter == self.numbers[2]:
            self.log_out()

        else:
            self.delete_account()

    def login_change(self):
        """Loginni o'zgartirish - Change login"""
        self.clear()
        new_login = input("New login: ").strip().lower()
        change_login = f"update username set login='{new_login}' where login='{self.old_login_password[0]}'"
        self.my_user.execute(change_login)
        self.mysql.commit()
        print("\n\t\t**>> Your login has been updated <<**\n")

    def password_change(self):
        """Parolni o'zgartirish - Change password"""
        self.clear()
        new_password = input("New login: ").strip().lower()
        change_password = f"update username set login='{new_password}' where login='{self.old_login_password[1]}'"
        self.my_user.execute(change_password)
        self.mysql.commit()
        print("\n\t\t**>> Your password has been updated <<**\n")

    def log_out(self):
        """Tizimdan chiqich - Log out"""
        self.selection()

    def delete_account(self):
        """Accountni o'chirish ucun metod - Method for deleting an account"""
        account_delete = f"delete from username where login='{self.old_login_password[0]}'"
        self.my_user.execute(account_delete)
        self.mysql.commit()
        print("\n\t\t**>> Deleted account <<**\n")

    def check_login_password(self, old_login, old_password):
        """Login va parolni tekshirib olish uchun metod - A method for verifying login and password"""
        take_out = f"select * from username where login='{old_login}' and password='{old_password}'"
        self.my_user.execute(take_out)
        select = self.my_user.fetchall()
        if select:
            return True
        else:
            return False

    @staticmethod
    def clear():
        """Ekranni tozalash metodi - Screen cleaning method"""
        os.system("clear")


user = User()
user.selection()

