# SolarSecurityTasks

<h2>task_1</h2>

<p>Для корректной работы необходимо наличие Python 3.5 или выше. (При разработке использовалась версия 3.6.2)</p>
<p>Для установки всех необходимых зависимостей необходимо в папке <b>task_1</b> выполнить команду</p>
<p><code> pip install -r requirements.txt </code></p>
<p>Для запуска сервера необходимо в папке <b>task_1</b> выполнить команду</p>
<p><code> pyhton run.py </code></p>
<p>которая запустит локальный сервер по адресу <a href="http://127.0.0.1:8080">127.0.0.1:8080</a></p>

<hr>

<h2>task_2</h2>

<p>Для корректной работы необходимо наличие Python 3.5 или выше. (При разработке использовалась версия 3.6.2)</p>
<p>Для установки всех необходимых зависимостей необходимо в папке <b>task_2</b> выполнить команду</p>
<p><code> pip install -r requirements.txt </code></p>
<p>Перед запуском скрипта в файле <code>config.py</code> необходимо указать данные подключения к базе данных (в данном случае используется PostgreSQL) в формате</p>
<p><code>postgresql://&lt;username&gt;:&lt;password&gt;@&lt;host[:port]&gt;/&lt;database&gt;</code></p>
<p>При запуске скрипта необходимо указать также относительный путь к файлу *.csv </p>
<p><code> pyhton csv_to_db.py path/to/file.csv </code></p>


