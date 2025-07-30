## SmartEstate

### About

Django app for real estate brokers. If you are a real estate broker, you can use this
to power your website, and the backend will allow you to manage your listings, apartments,
offers for sale, as well as potentials - renters, buyers, etc.

### Roadmap

This is a legacy project from ca. 3 years ago, which I am recently revisiting. It is not stable,
and not ready for production use, but I am working to release a stable version soon.
Until the stable version 1.0 appears, things can and will break between releases without notice.

### Installing/usage

#### Production

The latest stable image is available from Docker Hub under `sainthilaire/smartestate:latest`.

You can use it however you like. For example, the following _docker-compose.yml_
will set up a very minimal staging environment, but please change the credentials
to something more secure.

Also, for a real production environment, you will need SSL, but there
are many solutions for that.

```yaml
services:
  db:
    image: mysql:8.3
    restart: always
    environment:
      MYSQL_DATABASE: smartestate
      MYSQL_USER: smartestate
      MYSQL_PASSWORD: insecure-please-change
      MYSQL_ROOT_PASSWORD: insecure-please-change
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 10

  web:
    image: sainthilaire/smartestate:latest
    restart: always
    ports:
      - "80:8000"
    environment:
      DEBUG: 0
      SECRET_KEY: insecure-please-change
      ALLOWED_HOSTS: your-web-host.com
      CSRF_TRUSTED_ORIGINS: "https://*.your-web-host.com"
      DATABASE_ENGINE: django.db.backends.mysql
      DATABASE_HOST: db
      DATABASE_NAME: smartestate
      DATABASE_USER: smartestate
      DATABASE_PASSWORD: insecure-please-change
    depends_on:
      db:
        condition: service_healthy

volumes:
  db_data:
```

#### Local/dev via Docker-Compose

Easiest and preferred method. Clone the repository, and run:
```
docker compose up --detach --build
```

#### Local/dev via Django

* Install platform requirements (for the MySQL driver, see https://github.com/PyMySQL/mysqlclient)

  - Debian/Ubuntu
    ```
    apt install  python3-dev default-libmysqlclient-dev  build-essential  pkg-config
    ```

  - Red Hat / CentOS
    ```
    yum install python3-devel mysql-devel pkgconfig
    ```

  - Other distros / macOS / Windows: See the [docs for mysqlclient](https://github.com/PyMySQL/mysqlclient), you probably have to
    install similar libraries. Otherwise, if you don't need MySQL (ie. using SQLite locally),
    you can comment out `mysqlclient` from the dependencies in _pyproject.toml_ and it should work.

* Build app from source code:
```
pip install .
```

* Alternative: Install Python package:
```
pip install --upgrade smartestate
```

* `cp .env.example .env` and configure with appropriate values.
* `python manage.py migrate`
* `python manage.py createsuperuser`
* `python manage.py runserver`
* Unit tests: `python manage.py test`

Set up the cookie group in the Django admin, and make it optional for the cookie banner to appear.
