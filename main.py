import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

def connect_db():
    try:
        conn = psycopg2.connect(
            host='localhost',
            dbname='postgres',
            user='postgres',
            password='1234',
            port=5432
        )
        return conn
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
        return None
def create_tables():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            group_name VARCHAR(50) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS courses (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            student_id INT REFERENCES students(id),
            course_id INT REFERENCES courses(id),
            grade INT CHECK (grade >= 0 AND grade <= 100)
        );
        """)
        conn.commit()
        conn.close()
class ElectronicDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный дневник")
        self.setup_ui()
    def setup_ui(self):
        tab_control = ttk.Notebook(self.root)
        self.tab_management = ttk.Frame(tab_control)
        self.tab_view = ttk.Frame(tab_control)
        self.tab_students = ttk.Frame(tab_control)
        tab_control.add(self.tab_management, text="Управление")
        tab_control.add(self.tab_view, text="Просмотр оценок")
        tab_control.add(self.tab_students, text="Все студенты")
        tab_control.pack(expand=1, fill="both")
        self.setup_management_tab()
        self.setup_view_tab()
        self.setup_students_tab()
    def setup_management_tab(self):
        tk.Label(self.tab_management, text="Имя студента").grid(row=0, column=0, padx=10, pady=5)
        self.student_name_entry = tk.Entry(self.tab_management)
        self.student_name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.tab_management, text="Группа").grid(row=1, column=0, padx=10, pady=5)
        self.student_group_entry = tk.Entry(self.tab_management)
        self.student_group_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.tab_management, text="Добавить студента", command=self.add_student).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Label(self.tab_management, text="Название курса").grid(row=3, column=0, padx=10, pady=5)
        self.course_name_entry = tk.Entry(self.tab_management)
        self.course_name_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.tab_management, text="Добавить курс", command=self.add_course).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Label(self.tab_management, text="Имя студента").grid(row=5, column=0, padx=10, pady=5)
        self.grade_student_name_entry = tk.Entry(self.tab_management)
        self.grade_student_name_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(self.tab_management, text="Группа").grid(row=6, column=0, padx=10, pady=5)
        self.grade_student_group_entry = tk.Entry(self.tab_management)
        self.grade_student_group_entry.grid(row=6, column=1, padx=10, pady=5)
        tk.Label(self.tab_management, text="Курс").grid(row=7, column=0, padx=10, pady=5)
        self.grade_course_entry = tk.Entry(self.tab_management)
        self.grade_course_entry.grid(row=7, column=1, padx=10, pady=5)
        tk.Label(self.tab_management, text="Оценка (0-100)").grid(row=8, column=0, padx=10, pady=5)
        self.grade_entry = tk.Entry(self.tab_management)
        self.grade_entry.grid(row=8, column=1, padx=10, pady=5)
        tk.Button(self.tab_management, text="Добавить оценку", command=self.add_grade).grid(row=9, column=0, columnspan=2, pady=10)
    def setup_view_tab(self):
        tk.Label(self.tab_view, text="Имя студента").grid(row=0, column=0, padx=10, pady=5)
        self.view_student_name_entry = tk.Entry(self.tab_view)
        self.view_student_name_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.tab_view, text="Группа").grid(row=1, column=0, padx=10, pady=5)
        self.view_student_group_entry = tk.Entry(self.tab_view)
        self.view_student_group_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.tab_view, text="Показать оценки", command=self.view_grades).grid(row=2, column=0, columnspan=2, pady=10)
        self.grades_listbox = tk.Listbox(self.tab_view, width=50, height=15)
        self.grades_listbox.grid(row=3, column=0, columnspan=2, pady=10)
    def setup_students_tab(self):
        self.students_listbox = tk.Listbox(self.tab_students, width=60, height=20)
        self.students_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        tk.Button(self.tab_students, text="Обновить список", command=self.list_students).pack(pady=10)
    def add_student(self):
        name = self.student_name_entry.get()
        group = self.student_group_entry.get()
        if name and group:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (name, group_name) VALUES (%s, %s)", (name, group))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Студент добавлен")
                self.student_name_entry.delete(0, tk.END)
                self.student_group_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
    def add_course(self):
        course_name = self.course_name_entry.get()
        if course_name:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO courses (name) VALUES (%s)", (course_name,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Курс добавлен")
                self.course_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните название курса")
    def add_grade(self):
        student_name = self.grade_student_name_entry.get()
        student_group = self.grade_student_group_entry.get()
        course_name = self.grade_course_entry.get()
        grade = self.grade_entry.get()
        if student_name and student_group and course_name and grade:
            try:
                grade = int(grade)
                if grade < 0 or grade > 100:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Ошибка", "Оценка должна быть числом от 0 до 100")
                return
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM students WHERE name = %s AND group_name = %s",
                               (student_name, student_group))
                student = cursor.fetchone()
                if not student:
                    messagebox.showwarning("Ошибка", "Студент не найден")
                    conn.close()
                    return
                cursor.execute("SELECT id FROM courses WHERE name = %s", (course_name,))
                course = cursor.fetchone()
                if not course:
                    messagebox.showwarning("Ошибка", "Курс не найден")
                    conn.close()
                    return
                cursor.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (%s, %s, %s)",
                               (student[0], course[0], grade))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Оценка добавлена")
                self.grade_student_name_entry.delete(0, tk.END)
                self.grade_student_group_entry.delete(0, tk.END)
                self.grade_course_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
    def view_grades(self):
        student_name = self.view_student_name_entry.get()
        student_group = self.view_student_group_entry.get()
        if student_name and student_group:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT c.name, g.grade
                FROM grades g
                JOIN courses c ON g.course_id = c.id
                JOIN students s ON g.student_id = s.id
                WHERE s.name = %s AND s.group_name = %s
                """, (student_name, student_group))
                rows = cursor.fetchall()
                conn.close()

                self.grades_listbox.delete(0, tk.END)
                for row in rows:
                    self.grades_listbox.insert(tk.END, f"Курс: {row[0]}, Оценка: {row[1]}")
        else:
            messagebox.showwarning("Ошибка", "Введите имя и группу студента")
    def list_students(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT s.name, s.group_name, c.name, g.grade
            FROM students s
            LEFT JOIN grades g ON s.id = g.student_id
            LEFT JOIN courses c ON g.course_id = c.id
            ORDER BY s.name, s.group_name
            """)
            rows = cursor.fetchall()
            conn.close()

            self.students_listbox.delete(0, tk.END)
            for row in rows:
                student_info = f"Имя: {row[0]}, Группа: {row[1]}, Курс: {row[2] or 'Нет'}, Оценка: {row[3] or 'Нет'}"
                self.students_listbox.insert(tk.END, student_info)
if __name__ == "__main__":
    create_tables()

    root = tk.Tk()
    app = ElectronicDiaryApp(root)
    root.mainloop()
