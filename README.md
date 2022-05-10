# Shop project

Настоящий репозиторий содержит проект выполненный в рамках курса для самостоятельного изучения фреймворка Django. Код проекта
написан на языке Python 3.8, с использованием библиотек Django и Django REST framework, зависимости описаны в requirements.txt.

Проект работает с базой данных postgres.

Проект представляет REST API интернет-магазина. Описаны модели Category, Product, Bucket, Sale и Order.
Реализована регистрация новых пользователей интернет-магазина.


API

/product/

/product/{id}/

/bucket/

/bucket/add   
{
"id": 0,
"number": 2 }

/bucket/2/update {
"number": 2 }

/bucket/2 DELETE



