

import json
import pymysql
from pymysql import Error
import re

"""
0 - Активный
1 - Выполнен
2 - Провален
3 - Просрочен
"""
class Work():
    def is_connect(self):
        try:
            print("start")
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='1111',
                database='beedsssa'
            )
            if self.connection:
                print("connect")
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"{e}")


    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


    def validate_login(self, login):
        # Проверка на наличие специальных символов
        if not re.match("^[A-Za-z0-9_]+$", login):
            return False
        return True

    def create_children(self, login, password):
        if not self.validate_login(login):
            return "Ошибка: Специальные символы запрещены в логине ребенка."
        
        self.is_connect()
        try:
            # Проверка уникальности логина
            self.cursor.execute("SELECT COUNT(*) FROM children WHERE login = %s", (login,))
            count = self.cursor.fetchone()[0]
            if count > 0:
                return f"Ошибка: Логин ребенка '{login}' уже существует."
            self.cursor.execute("""INSERT INTO children (login, password, access_level) 
            VALUES (%s, %s, %s)""", (login, password, 0))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()


    def get_children_by_parent_login(self, parent_login):
        self.is_connect()
        try:
            # Получаем поле login_children из таблицы parents
            self.cursor.execute("SELECT login_children FROM parents WHERE login = %s", (parent_login,))
            result = self.cursor.fetchone()

            if result:
                # Извлекаем логины детей
                login_children = result[0].split(',')  # Предполагаем, что логины разделены запятыми
                
                # Получаем данные из таблицы children
                self.cursor.execute("SELECT * FROM children WHERE login IN (%s)" % ','.join(['%s'] * len(login_children)), tuple(login_children))
                children_result = self.cursor.fetchall()
                children_result = list(children_result)
                children_result = json.dumps(children_result)
                return children_result  # Возвращаем результат
            else:
                return f"Ошибка: Родитель с логином '{parent_login}' не найден."
        except Error as e:
            return e
        finally:
            self.disconnect()


    def create_parents(self, login, password):
        if not self.validate_login(login):
            return "Ошибка: Специальные символы запрещены в логине родителя."
        
        self.is_connect()
        try:
            # Проверка уникальности логина
            self.cursor.execute("SELECT COUNT(*) FROM parents WHERE login = %s", (login,))
            count = self.cursor.fetchone()[0]
            if count > 0:
                return f"Ошибка: Логин родителя '{login}' уже существует."
            self.cursor.execute("""INSERT INTO parents (login, password, login_children, access_level) 
            VALUES (%s, %s, %s, %s)""", (login, password, None, 1))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()


    def get_children_by_teacher_login(self, teacher_login):
        self.is_connect()
        try:
            # Получаем поле login_children из таблицы teacher
            self.cursor.execute("SELECT login_children FROM teacher WHERE login = %s", (teacher_login,))
            result = self.cursor.fetchone()
            print(result)

            if result:
                    
                # Извлекаем логины детей
                login_children = result[0]  # Предполагаем, что логины разделены запятыми
                
                    
                # Получаем данные из таблицы children
                self.cursor.execute("SELECT * FROM children WHERE login IN (%s)" % ','.join(['%s'] * len(login_children)), tuple(login_children))
                
                try:
                    children_result = self.cursor.fetchall()
                    children_result = list(children_result)
                    children_result = json.dumps(children_result)
                except:
                    children_result ={}

                return children_result  # Возвращаем результат
            else:
                return f"Ошибка: Учитель с логином '{teacher_login}' не найден."
        except Error as e:
            return e
        finally:
            self.disconnect()


    def create_teacher(self, login, password):
        if not self.validate_login(login):
            return "Ошибка: Специальные символы запрещены в логине учителя."
        
        self.is_connect()
        try:
            # Проверка уникальности логина
            self.cursor.execute("SELECT COUNT(*) FROM teacher WHERE login = %s", (login,))
            count = self.cursor.fetchone()[0]
            if count > 0:
                return f"Ошибка: Логин учителя '{login}' уже существует."
            self.cursor.execute("""INSERT INTO teacher (login, password, login_children) 
            VALUES (%s, %s, %s)""", (login, password, None))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()

    def login_children(self, login, password):
        self.is_connect()
        try:
            self.cursor.execute("SELECT access_level FROM children WHERE login = %s AND password = %s", (login, password))
            result = self.cursor.fetchone()
            if result:
                return {'lvl': result[0], 'login': login}
            return "Ошибка: Неверный логин или пароль для детей."
        except Error as e:
            return e
        finally:
            self.disconnect()


    def login_parents(self, login, password):
        self.is_connect()
        try:
            self.cursor.execute("SELECT access_level FROM parents WHERE login = %s AND password = %s", (login, password))
            result = self.cursor.fetchone()
            if result:
                return {'lvl': result[0], 'login': login}
            return "Ошибка: Неверный логин или пароль для родителей."
        except Error as e:
            return e
        finally:
            self.disconnect()


    def login_teacher(self, login, password):
        self.is_connect()
        try:
            self.cursor.execute("SELECT access_level FROM teacher WHERE login = %s AND password = %s", (login, password))
            result = self.cursor.fetchone()
            if result:
                return {'lvl': result[0], 'login': login}
            return "Ошибка: Неверный логин или пароль для учителей."
        except Error as e:
            return e
        finally:
            self.disconnect()


    def update_teach(self, login, login_children):
        self.is_connect()
        try:
            # Получаем текущее значение поля login_children
            self.cursor.execute("SELECT login_children FROM teacher WHERE login = %s", (login,))
            result = self.cursor.fetchone()
            
            if result:
                current_login_children = result[0]
                # Проверяем, если текущее значение не пустое, добавляем запятую
                if current_login_children:
                    new_login_children = current_login_children + ',' + login_children
                else:
                    new_login_children = login_children

                # Обновляем поле login_children
                self.cursor.execute("UPDATE teacher SET login_children = %s WHERE login = %s", (new_login_children, login))
                self.connection.commit()
                return True
            else:
                return f"Ошибка: Учитель с логином '{login}' не найден."
        except Error as e:
            return e
        finally:
            self.disconnect()

    def update_parents(self, login, login_children):
        self.is_connect()
        try:
            # Получаем текущее значение поля login_children
            self.cursor.execute("SELECT login_children FROM parents WHERE login = %s", (login,))
            result = self.cursor.fetchone()
            
            if result:
                current_login_children = result[0]
                # Проверяем, если текущее значение не пустое, добавляем запятую
                if current_login_children:
                    new_login_children = current_login_children + ',' + login_children
                else:
                    new_login_children = login_children

                # Обновляем поле login_children
                self.cursor.execute("UPDATE parents SET login_children = %s WHERE login = %s", (new_login_children, login))
                self.connection.commit()
                return True
            else:
                return f"Ошибка: Родитель с логином '{login}' не найден."
        except Error as e:
            return e
        finally:
            self.disconnect()

    def create_task(self, login_children, access_level, task_name, task_text, status, deadline, from_login):
        self.is_connect()
        try:
            self.cursor.execute("""INSERT INTO task (login_children, access_level, task_name, from_, task_text, status, deadline) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", (login_children, access_level, task_name, from_login, task_text, status, deadline))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()

    def update_task_status(self, task_id, new_status):
        self.is_connect()
        try:
            self.cursor.execute("UPDATE task SET status = %s WHERE id_task = %s", (new_status, task_id))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()


    def inset_profile_teacher_task(self, login):
        self.is_connect()
        try:
            self.cursor.execute("""SELECT * FROM task WHERE from_ = %s""", (login,))
            result = self.cursor.fetchall()
            list_result = list(result)
            json_data = json.dumps(list_result)
            return json_data
        except Error as e:
            return e
        finally:
            self.disconnect()


    def delete_task(self, task_id):
        self.is_connect()
        try:
            self.cursor.execute("DELETE FROM task WHERE id_task = %s", (task_id,))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()



    def create_note(self, login_children, access_level, notes_text):
        self.is_connect()
        try:
            self.cursor.execute("""INSERT INTO notes (login_children, access_level, notes_text) 
            VALUES (%s, %s, %s)""", (login_children, access_level, notes_text))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()


    def delete_note(self, note_id):
        self.is_connect()
        try:
            self.cursor.execute("DELETE FROM notes WHERE note_id = %s", (note_id,))
            self.connection.commit()
            return True
        except Error as e:
            return e
        finally:
            self.disconnect()
            

    def get_all_tasks(self, login):
        self.is_connect()
        try:
            self.cursor.execute("SELECT * FROM task WHERE login_children = %s", (login,))
            columns = [column[0] for column in self.cursor.description]
            rows = self.cursor.fetchall()
            tasks = [dict(zip(columns, row)) for row in rows]
            return tasks
        except Error as e:
            return e
        finally:
            self.disconnect()



    def check(self,login):
        self.is_connect()
        try:
            self.cursor.execute("SELECT * FROM task WHERE login_children = %s", (login,))
            print(self.cursor.fetchone())
        except Error as e:
            print(e)


    def get_notes_by_login(self, login_children):
        self.is_connect()
        try:
            self.cursor.execute("SELECT * FROM notes WHERE login_children = %s", (login_children,))
            notes = self.cursor.fetchall()
            return notes
        except Error as e:
            return e
        finally:
            self.disconnect()


if __name__ == "__main__":
    W = Work()
    result = W.get_children_by_teacher_login("Os")
    print(result)







           