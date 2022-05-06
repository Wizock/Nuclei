class student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def say_hi():
        return "Hello"


jamal = student("Jamal", 20)


print(jamal.say_hi())
