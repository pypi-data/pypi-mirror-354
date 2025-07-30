# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_cassandra_engine',
 'django_cassandra_engine.base',
 'django_cassandra_engine.management',
 'django_cassandra_engine.management.commands',
 'django_cassandra_engine.models',
 'django_cassandra_engine.rest',
 'django_cassandra_engine.sessions',
 'django_cassandra_engine.sessions.backends']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.2,<6.0', 'scylla-driver>=3.29,<4.0']

setup_kwargs = {
    'name': 'django-cassandra-engine',
    'version': '1.10.0',
    'description': 'Django Cassandra Engine',
    'long_description': '\n# Django Cassandra Engine - the Cassandra backend for Django #\n\nAll tools you need to start your journey with Apache Cassandra and Django Framework!\n\n[![Latest version](https://img.shields.io/pypi/v/django-cassandra-engine.svg "Latest version")](https://pypi.python.org/pypi/django-cassandra-engine/)\n![workflow](https://github.com/r4fek/django-cassandra-engine/actions/workflows/tox.yml/badge.svg)\n\nDiscord: https://discord.gg/pxunMGmDNc\n## Features ##\n\n* integration with latest `python-driver` and optionally `dse-driver` from DataStax\n* working `flush`, `migrate`, `sync_cassandra`, `inspectdb` and\n  `dbshell` commands\n* support for creating/destroying test database\n* accepts all `Cqlengine` and `cassandra.cluster.Cluster` connection options\n* automatic connection/disconnection handling\n* works well along with relational databases (as secondary DB)\n* storing sessions in Cassandra\n* working django forms\n* usable admin panel with Cassandra models\n* support DataStax Astra cloud hosted Cassandra\n\n## Sponsors ##\nHelp support ongoing development and maintenance by [sponsoring Django Cassandra Engine](https://github.com/sponsors/r4fek).\n\n### Our Sponsors: ###\n<table><tr>\n<td align="center" width="300" ><a href="https://astra.dev/3xPljcu"><img src="https://www.datastax.com/sites/default/files/2021-07/astra-negative-square.png" width="90" height="90" alt="Astra DB" /><br />Astra DB</a><br/>Use Django with DataStax Astra DB - built on Apache Cassandra.</td>\n<td align="center" width="300" ><a href="https://github.com/NoiSek"><img src="https://avatars.githubusercontent.com/u/631328?v=4" width="90" height="90" alt="NoiSek" /><br/>NoiSek</a></td>\n</tr></table>\n\n\n## Installation ##\n\nRecommended installation:\n\n    pip install django-cassandra-engine\n\n## Basic Usage ##\n\n1. Add `django_cassandra_engine` to `INSTALLED_APPS` in your `settings.py` file:\n\n        INSTALLED_APPS = (\'django_cassandra_engine\',) + INSTALLED_APPS\n\n2. Change `DATABASES` setting:\n\n        DATABASES = {\n            \'default\': {\n                \'ENGINE\': \'django_cassandra_engine\',\n                \'NAME\': \'db\',\n                \'TEST_NAME\': \'test_db\',\n                \'HOST\': \'db1.example.com,db2.example.com\',\n                \'OPTIONS\': {\n                    \'replication\': {\n                        \'strategy_class\': \'SimpleStrategy\',\n                        \'replication_factor\': 1\n                    }\n                }\n            }\n        }\n\n3. Define some model:\n\n        # myapp/models.py\n\n        import uuid\n        from cassandra.cqlengine import columns\n        from django_cassandra_engine.models import DjangoCassandraModel\n\n        class ExampleModel(DjangoCassandraModel):\n            example_id    = columns.UUID(primary_key=True, default=uuid.uuid4)\n            example_type  = columns.Integer(index=True)\n            created_at    = columns.DateTime()\n            description   = columns.Text(required=False)\n\n4. Run `./manage.py sync_cassandra`\n5. Done!\n\n## Connect to Cassandra with a Cloud Config bundle ##\nTo connect to a hosted Cassandra cluster that provides a secure connection bundle (ex. DataStax Astra) change the `DATABASES` setting of your settings.py:\n\n        DATABASES = {\n            \'default\': {\n                \'ENGINE\': \'django_cassandra_engine\',\n                \'NAME\': \'keyspace_name\',\n                \'TEST_NAME\': \'table_name\',\n                \'USER\': \'token\',\n                \'PASSWORD\': token_value,\n                \'OPTIONS\': {\n                    \'connection\': {\n                        \'cloud\': {\n                            \'secure_connect_bundle\': \'/path/to/secure/bundle.zip\'\n                        },\n                    }\n                }\n            }\n        }\n\n## Documentation ##\n\nThe documentation can be found online [here](http://r4fek.github.io/django-cassandra-engine/).\n\n## License ##\nCopyright (c) 2014-2024, [Rafał Furmański](https://linkedin.com/in/furmanski).\n\nAll rights reserved. Licensed under BSD 2-Clause License.\n',
    'author': 'Rafał Furmański',
    'author_email': 'r.furmanski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/r4fek/django-cassandra-engine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
