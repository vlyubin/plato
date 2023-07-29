from collections import namedtuple

Person = namedtuple("Person", "name description topics")

people = [
    Person("Donald Trump", "former president, businessman and billionaire", [("Donald Trump is the best president in American History", True), ("Vodka is better than wine", True), ("Golf is better than soccer", True)]),
]

