Gold (Золото)
=================

Скрипт получает текущую стоимость 10-граммового золотого слитка с сайта Сбербанка (в .xls файле).
После этого он сравниваниет текущую стоимость со стоимостью покупки слитка, выражает её в рублях, процентах и на графике в Jupyter Notebook отображает изменения стоимости с момента покупки до текущего дня. 
Данные для построения графика изменения стоимости берутся из csv файла, куда текущие данные сохраняются скриптом каждый раз, когда скрипт получает новую стоимость с сайта.

Время получения этих данных вручную: 1 мин. 36 сек.
Время получения этих данных с помощью скрипта: 48 сек. (в 2 раза быстрее(!) + возможность увидеть график)

***********


Используемые инструменты и модули:
```
    Python, Requests, Pandas, Matplotlib, Json, JupyterNotebook

```

Запуск скрипта
---------

Aктивируйте виртуальное окружение:

```
    На Windows: env\Scripts\activate
```
```
    На Mac или Linux: source env/bin/activate
```
После этого в виртуальном окружении выполните:

```
    jupyter notebook
=======