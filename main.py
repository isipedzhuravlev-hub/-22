import pickle
import os

class Book:
    def __init__(self, title, author, status="available"):
        self.title = title
        self.author = author
        self.status = status

    def __str__(self):
        return f"{self.title} - {self.author} [{self.status}]"

class Person:
    def __init__(self, name):
        self._name = name

class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__books = []

    def add_book(self, title):
        if title not in self.__books:
            self.__books.append(title)

    def return_book(self, title):
        if title in self.__books:
            self.__books.remove(title)

    def get_books(self):
        return self.__books[:]

class Librarian(Person):
    pass

DATA_FILE = "library_data.pkl"

def load_data():
    if not os.path.exists(DATA_FILE):
        return [], {}
    try:
        with open(DATA_FILE, "rb") as f:
            data = pickle.load(f)
        return data.get("books", []), data.get("users", {})
    except:
        return [], {}

def save_data(books, users):
    try:
        with open(DATA_FILE, "wb") as f:
            pickle.dump({"books": books, "users": users}, f)
    except:
        pass

books, users = load_data()

print("\nБиблиотека")
print("1 - Библиотекарь")
print("2 - Пользователь")
print("0 - Выход")

choice = input(">>> ").strip()

if choice == "1":
    name = input("Имя библиотекаря: ").strip()
    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Зарегистрировать пользователя")
        print("4. Список пользователей")
        print("5. Список книг")
        print("0. Выход")
        cmd = input(">>> ").strip()

        if cmd == "1":
            title = input("Название: ").strip()
            author = input("Автор: ").strip()
            books.append(Book(title, author))
            print("Книга добавлена!")
        elif cmd == "2":
            title = input("Название: ").strip()
            books[:] = [b for b in books if b.title != title]
            print("Книга удалена")
        elif cmd == "3":
            uname = input("Имя пользователя: ").strip()
            users[uname] = User(uname)
            print("Пользователь зарегистрирован")
        elif cmd == "4":
            print(list(users.keys()) if users else "Нет пользователей")
        elif cmd == "5":
            for b in books:
                print(b)
        elif cmd == "0":
            break

elif choice == "2":
    name = input("Ваше имя: ").strip()
    if name in users:
        user = users[name]
        while True:
            print("\n1. Доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("0. Выход")
            cmd = input(">>> ").strip()

            if cmd == "1":
                for b in books:
                    if b.status == "available":
                        print(b)
            elif cmd == "2":
                title = input("Название книги: ").strip()
                for b in books:
                    if b.title == title and b.status == "available":
                        b.status = "issued"
                        user.add_book(title)
                        print("Книга выдана!")
                        break
                else:
                    print("Книга не найдена или уже выдана")
            elif cmd == "3":
                title = input("Название книги: ").strip()
                for b in books:
                    if b.title == title:
                        b.status = "available"
                        user.return_book(title)
                        print("Книга возвращена")
                        break
            elif cmd == "4":
                print(user.get_books() or "Книг нет")
            elif cmd == "0":
                break

# Сохранение и пауза
save_data(books, users)
print("\nДанные сохранены.")

input("\nНажмите Enter, чтобы закрыть окно...")