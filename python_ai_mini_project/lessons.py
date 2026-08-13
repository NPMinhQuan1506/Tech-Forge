LESSONS = [
    {
        "id": 1,
        "title": "Setup va chay file Python",
        "content": """
Muc tieu:
- Cai Python 3.12 hoac 3.13.
- Kiem tra bang `python --version` hoac `py --version`.
- Chay file bang `python main.py`.

Vi du:
print("Hello, Python")
""".strip(),
    },
    {
        "id": 2,
        "title": "Indentation va comment",
        "content": """
Python dung thut le de tao block code, thuong la 4 dau cach.

Dung:
if age >= 18:
    print("Adult")

Comment mot dong dung dau #.
""".strip(),
    },
    {
        "id": 3,
        "title": "Variable va data type",
        "content": """
Python khong can khai bao kieu truoc.

Vi du:
name = "Quan"
age = 26
salary = 31_000_000
is_developer = True

Nen dat ten bien theo snake_case.
""".strip(),
    },
    {
        "id": 4,
        "title": "Number, boolean va comparison",
        "content": """
Toan tu so hoc:
+, -, *, /, //, %, **

Boolean dung True va False.
So sanh dung ==, !=, >, <, >=, <=.
Logic dung and, or, not.
""".strip(),
    },
    {
        "id": 5,
        "title": "String",
        "content": """
String co the dung nhay kep hoac nhay don.

Vi du f-string:
name = "Quan"
message = f"Hello, {name}"

Indexing:
text = "Python"
text[0] la "P"
text[-1] la "n"
text[0:3] la "Pyt"
""".strip(),
    },
    {
        "id": 6,
        "title": "List, tuple, dict, set",
        "content": """
list: thay doi duoc, vi du [1, 2, 3]
tuple: khong thay doi, vi du (1, 2)
dict: key-value, vi du {"name": "Quan"}
set: tap hop khong trung lap, vi du {1, 2, 3}
""".strip(),
    },
    {
        "id": 7,
        "title": "Input va output",
        "content": """
In ra man hinh:
print("Hello")

Nhap tu ban phim:
name = input("Name: ")

Luu y: input() luon tra ve string.
Muon lay so nguyen thi dung int(input(...)).
""".strip(),
    },
    {
        "id": 8,
        "title": "Control flow",
        "content": """
Python dung if, elif, else.

Vi du:
if score >= 8:
    print("Excellent")
elif score >= 6.5:
    print("Good")
else:
    print("Need improvement")
""".strip(),
    },
    {
        "id": 9,
        "title": "Loop",
        "content": """
for dung de lap qua list, range, dict...
while dung khi lap theo dieu kien.

Cong cu hay gap:
- range()
- enumerate()
- zip()
- break
- continue
- pass
""".strip(),
    },
    {
        "id": 10,
        "title": "Function",
        "content": """
Function giup chia code thanh phan nho.

Vi du:
def add(a: int, b: int) -> int:
    return a + b

Type hint giup code de doc hon nhung khong ep kieu tai runtime.
""".strip(),
    },
    {
        "id": 11,
        "title": "Exception va file IO",
        "content": """
Bat loi:
try:
    age = int(input("Age: "))
except ValueError:
    print("Age must be a number")

Doc/ghi file nen dung with open(..., encoding="utf-8").
""".strip(),
    },
    {
        "id": 12,
        "title": "Module, class va dataclass",
        "content": """
Module la file Python co the import.
Pattern hay dung:
if __name__ == "__main__":
    main()

Class gom data va method.
@dataclass giup tao class data nhanh gon.
""".strip(),
    },
]


def get_lesson(lesson_id: int) -> dict | None:
    for lesson in LESSONS:
        if lesson["id"] == lesson_id:
            return lesson
    return None
