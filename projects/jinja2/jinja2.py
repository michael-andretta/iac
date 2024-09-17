### Import Libraries ###
from jinja2 import Environment, FileSystemLoader

### Variables ###
max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Alice", "score": 90},
    {"name": "Bob", "score": 80},
    {"name": "Charlie", "score": 70},
    {"name": "David", "score": 60},
    {"name": "Eve", "score": 50},
]

### Jinja2 Template ###
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("message.txt")

### Render Template ###
for student in students:
    filename = f"message_{student['name'].lower()}.txt"
    content = template.render(
        student=student, 
        max_score=max_score, 
        test_name=test_name
    )

    with open(filename,  mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"Message for {student['name']} has been created.")
