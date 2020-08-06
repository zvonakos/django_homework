from django.shortcuts import render  # noqa
from django.http import HttpResponse  # noqa

import random  # noqa
import string  # noqa

from students.models import Student  # noqa
from faker import Faker  # noqa


def generate_password(length: int = 10) -> str:
    choices = string.ascii_letters + string.digits + string.punctuation
    password = ''
    for _ in range(length):
        password += random.choice(choices)

    return password


def generate_one_student() -> Student:
    fake = Faker()
    name, surname = fake.name().split()
    new_student = Student.objects.create(first_name=name, last_name=surname, age=random.randint(0, 100))

    return new_student


def hello_world(request):
    return HttpResponse(
        generate_password(
            int(request.GET['length'])
        )
    )


def students(request):
    count = Student.objects.count()
    students_queryset = Student.objects.all()
    response = f'students: {count}<br/>'
    for student in students_queryset:
        response += student.info() + '<br/>'
    return HttpResponse(response)


def generate_student(request) -> HttpResponse:
    return HttpResponse(f'One new user was created: {generate_one_student().info()}')


def generate_students(request) -> HttpResponse:
    count = request.GET.get('count', '10')
    if not count.isdigit():
        return HttpResponse('Incorrect request!')

    count = int(count)
    if count <= 0 or count > 100:
        return HttpResponse(f'Incorrect count value: {count}')

    new_users = ''
    for i in range(count):
        new_one = generate_one_student()
        new_users += new_one.info() + '<br/>'

    return HttpResponse(new_users)