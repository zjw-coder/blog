# Flask完整项目：Blog

```python
# manage.py代码
import os
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import create_app

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

> 由于代码较多，可下载查看。
>
> 