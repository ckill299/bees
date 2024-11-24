from datetime import datetime
import pymysql
from pymysql import Error



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






class SumTask():
    def __init__(self):
        self.BD = Work()

    def curect_data(self):
        curect_data = datetime.now()
        self.currect_month = curect_data.month
        self.currect_year = curect_data.year

    def task_filter(self, login):
        self.curect_data()
        result = self.BD.get_all_tasks(login)
    
        task_sum = {month: 0 for month in range(1, 13)}

        for res in result:
            print(res)
            date_object = datetime.strptime(res["deadline"], "%d.%m.%Y %H:%M")
            if date_object.year == self.currect_year:
                task_sum[date_object.month] += 1
        return {"task-sum": task_sum}

if __name__ == "__main__":
    St = SumTask()
    print(St.task_filter("A"))