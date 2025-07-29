# Ct Redis Cache Lib

A specialized library developed by Credenti for efficient Redis caching in Flask applications.

## Features

- Decorator-based caching for Flask endpoints and functions
- Configurable Redis connection pooling
- Supports cache key templating with nested attribute access
- Easy integration with Flask app lifecycle

## Installation

```sh
pip install ct-redis-cache-lib
```

## Configuration

Add the following to your Flask app configuration:

```python
app.config['REDIS_CACHE'] = True  # Enable or disable Redis caching
app.config['REDIS_CACHE_EXPIRE_TIME'] = 60  # Default cache expiration time in seconds
app.config['CACHE_REDIS_HOST'] = 'localhost'  # Redis host
app.config['CACHE_REDIS_PORT'] = 6379         # Redis port
app.config['CACHE_CLIENT_NAME'] = 'my-client' # Redis client name
```

## Usage

```python
from flask import Flask
from ct_redis_cache_lib import init_cache
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize the Redis cache
ct_redis = init_cache(app, logger)

@app.route('/idle_time')
@ct_redis.cache(template_cache_key='idle_time_value:$idle_time', field='$idle_time')
def get_idle_time_value(idle_time: str):
    # Your function logic here
    return {'idle_time': idle_time}
```

### Updating a Cache Entry

Update a cache entry directly using the `update` method.  
**Note:** Pass the actual, fully-resolved cache key (not a template):

```python
ct_redis.update(
    cache_key='idle_time_value:123',  # Actual cache key
    field='some_field',
    value={'idle_time': 123},
    is_global=False,  # or True if the key is global
    expire_time=120   # optional, in seconds
)
```

### Deleting a Cache Entry

Delete a cache entry using the `delete` method.  
**Note:** Pass the actual, fully-resolved cache key (not a template):

```python
ct_redis.delete(
    cache_key='idle_time_value:123',  # Actual cache key, not a template
    field='some_field',
    is_global=False  # or True if the key is global
)
```

### Committing and Resetting Cache

Commit cache writes after each request:

```python
@app.after_request
def after_request(response):
    ct_redis.commit(response)
    return response
```

Reset cache if you need to roll back changes:

```python
ct_redis.reset()
```

## Cache Key Specification

- Use `$` to access nested dictionary or object attributes in cache keys.
  - Example for dict: `template_cache_key='idle_time_value:$dict[key1][key2]'`
  - Example for object: `template_cache_key='idle_time_value:$obj.key1.key2'`
- Use static strings directly: `template_cache_key='idle_time'`