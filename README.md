# Shop project

Настоящий репозиторий содержит проект выполненный в рамках курса для самостоятельного изучения фреймворка Django. Код проекта
написан на языке Python 3.8, с использованием библиотек Django и Django REST framework, зависимости описаны в requirements.txt.

Проект работает с базой данных postgres.

Проект представляет REST API интернет-магазина. Описаны модели Category, Product, Bucket, Sale и Order. Реализована регистрация
новых пользователей интернет-магазина.

## Описание API

### Category

Модель Category представляет собой Категорию товаров, представленных в интернет-магазине. Категория имеет одну родительскую
категорию, которая может быть пустой.

category/

Для неавторизованных пользователей и пользователей с флагом is_staff = False, доступен только запрос GET, который возвращает
список категорий. Для авторизованных пользователей с флагом is_staff = True, доступен так же POST запрос для создания категории,
данные принимаются в виде:

data = {
'name': name,
'parent': parent }

category/{category.id}

Для неавторизованных пользователей и пользователей с флагом is_staff = False доступна информация о выбранной категории. Для
авторизованных пользователей с флагом is_staff = True доступны PUT и PATCH запросы.

### Product

Модель Product представляет собой Товар, представленный в интернет-магазине. Основные атрибуты товары это name, price,
description и categories. Продукт должен относиться как минимум к одной категории.

product/

Для неавторизованных пользователей и пользователей с is_staff = False доступен только запрос GET. Для пользователей с is_staff =
True доступны запросы GET и POST.

