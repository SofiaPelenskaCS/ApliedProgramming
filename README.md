1.за допомогою pyenv роблю версію python 3.6.3 глобальною

2.створюю віртуальне середовище venv за допомогою команди: python -m venv venv

3.активую середовище командою: source venv/bin/activate

4.інсталюю flask та gunicorn за допомогою: pip install flask pip install gunicorn

5.створюю requirements.txt командою: pip freeze > requirements.txt

6.програма реалізована за адресою http://0.0.0.0:5000/api/v1/hello-world-21/

7.щоб запустити програму за допомогою gunicorn використовую команду: gunicorn --bind 0.0.0.0:5000 hello:app
