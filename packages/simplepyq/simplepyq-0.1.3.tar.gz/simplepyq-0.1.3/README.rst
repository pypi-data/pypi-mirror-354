==========
simplepyq
==========

Queueing tasks in Python doesn't have to be complicated.

Overview
--------

`simplepyq` is a lightweight task queuing library designed for small Python projects that require background task
execution without the complexity of heavy tools like Celery, Airflow, or Redis. It uses SQLite for task
persistence, ensuring tasks survive application restarts, and provides features like task channels, automatic
retries, and dynamic task deferral. With minimal dependencies, `simplepyq` is easy to set up and ideal for
applications needing simple, reliable task queuing.

Features
--------

- **Channels**: Organize tasks by associating them with specific functions, enabling grouped task processing.
- **Persistence**: Store tasks in a SQLite database to ensure they are not lost during application restarts or crashes.
- **Retries**: Automatically retry failed tasks a specified number of times, improving resilience for transient errors.
- **DelayException**: Dynamically defer tasks for a specified duration, allowing flexible scheduling based on runtime conditions.
- **Simple Setup**: Minimal dependencies and straightforward API, requiring only Python and `msgpack`.
- **Task Management**: Tools to clear failed tasks, requeue them, or remove entire channels, providing control over task lifecycle.

Concepts
--------

Channels
~~~~~~~~
Channels in `simplepyq` allow you to group tasks by their purpose or associated function. Each channel is linked
to a specific Python function that processes tasks, and you can configure the number of worker threads for each
channel. This is useful for separating different types of tasks, such as "email" for sending emails and
"image_processing" for handling image uploads, ensuring organized and parallel task execution.

Persistence
~~~~~~~~~~~
Tasks are stored in a SQLite database, which provides lightweight persistence without requiring external systems.
Each task is saved with its channel, arguments, status (pending, running, delayed, done, or failed), retries, and
optional delay timestamp. This ensures tasks are not lost if the application restarts, making `simplepyq` reliable
for long-running operations.

Retries
~~~~~~~
When a task raises an exception, `simplepyq` can automatically retry it based on a specified retry count. This is
particularly useful for handling transient failures. If retries are exhausted, the task is marked as "failed" for
later inspection or requeuing.

DelayException
~~~~~~~~~~~~~~
The `DelayException` allows tasks to be deferred dynamically by raising an exception with a specified delay in seconds.
This is useful for scenarios like rate-limited APIs, where a task needs to wait before retrying, or for scheduling tasks
to run at a later time. The task is marked as "delayed" and automatically requeued when the delay period expires.

Task Management
~~~~~~~~~~~~~~~
`simplepyq` provides methods to manage tasks effectively:
- `clear_failed`: Removes failed tasks from the database.
- `requeue_failed`: Requeues failed tasks with their original or a new retry count.
- `remove_channel`: Deletes a channel and all its tasks.
- `stop` and `run_until_complete`: Control the scheduler’s execution, either running tasks in the background or until all tasks are complete.

Installation
------------

Install `simplepyq` via pip:

.. code-block:: bash

    pip install simplepyq

Usage Examples
--------------

Below are examples demonstrating each feature of `simplepyq`, designed to highlight its capabilities in real-world scenarios.

1. Basic Task Queuing with Channels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Organize tasks into a channel for web scraping, processing URLs in the background.

.. code-block:: python

    from simplepyq import SimplePyQ

    def scrape_url(args):
        url = args["url"]
        print(f"Scraping {url}")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("scrape", scrape_url, max_workers=2)  # Two workers for parallel scraping
    scheduler.enqueue("scrape", {"url": "https://example.com"})
    scheduler.enqueue("scrape", {"url": "https://example.org"})
    scheduler.start()  # Runs in the background
    # Tasks are processed concurrently by two worker threads

**Explanation**: The `scrape` channel is created with a function to process URLs, and two workers allow parallel execution. Tasks are enqueued with arguments and processed asynchronously.

2. Task Retries for Resilience
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Handle transient failures, such as network issues, with automatic retries.

.. code-block:: python

    from simplepyq import SimplePyQ
    import requests

    def fetch_data(args):
        url = args["url"]
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch data")
        print(f"Fetched data from {url}")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("fetch", fetch_data)
    scheduler.enqueue("fetch", {"url": "https://api.example.com/data"}, retries=3)  # Retry up to 3 times
    scheduler.run_until_complete()  # Runs until all tasks are complete

**Explanation**: If the API call fails, the task is retried up to three times before being marked as failed, ensuring resilience against temporary issues.

3. Dynamic Task Deferral with DelayException
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defer tasks dynamically, useful for rate-limited APIs.

.. code-block:: python

    from simplepyq import SimplePyQ, DelayException

    def call_api(args):
        url = args["url"]
        response = requests.get(url)
        if response.status_code == 403:
            raise DelayException(60)  # Wait 60 seconds before retrying
        print(f"Calling {url}")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("api", call_api)
    scheduler.enqueue("api", {"url": "https://api.example.com/rate_limit"})
    scheduler.start()  # Task will be deferred for 60 seconds if rate-limited

**Explanation**: The `DelayException` defers the task for 60 seconds, allowing compliance with rate limits or scheduling retries at a later time.

4. Clearing Failed Tasks
~~~~~~~~~~~~~~~~~~~~~~~~
Remove failed tasks to clean up the database.

.. code-block:: python

    from simplepyq import SimplePyQ

    def risky_task(args):
        raise Exception("Task failed intentionally")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("risky", risky_task)
    scheduler.enqueue("risky", {"data": "test"}, retries=1)
    scheduler.run_until_complete()  # Task fails after one retry
    scheduler.clear_failed("risky")  # Remove failed tasks for the 'risky' channel

**Explanation**: After the task fails and retries are exhausted, `clear_failed` removes it from the database, keeping it clean.

5. Requeuing Failed Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~
Requeue failed tasks for another attempt.

.. code-block:: python

    from simplepyq import SimplePyQ

    attempts = 0

    def flaky_task(args):
        global attempts
        if attempts < 2:  # Fail on first attempt
            attempts += 1
            raise Exception("Temporary failure")
        print("Task succeeded")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("flaky", flaky_task)
    scheduler.enqueue("flaky", {}, retries=0)
    scheduler.run_until_complete()  # Task fails
    scheduler.requeue_failed("flaky", retries=1)  # Requeue with one retry
    scheduler.run_until_complete()  # Task succeeds on second attempt

**Explanation**: Failed tasks are requeued with a new retry count, allowing recovery from temporary issues without manual intervention.

6. Removing a Channel
~~~~~~~~~~~~~~~~~~~~~
Delete a channel and its tasks when no longer needed.

.. code-block:: python

    from simplepyq import SimplePyQ

    def temp_task(args):
        print(f"Processing {args['data']}")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("temp", temp_task)
    scheduler.enqueue("temp", {"data": "test"})
    scheduler.run_until_complete()
    scheduler.remove_channel("temp")  # Removes channel and all its tasks

**Explanation**: The `temp` channel and its tasks are removed, useful for cleanup when a task type is no longer needed.

7. Running Until Completion
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Process all tasks synchronously until complete.

.. code-block:: python

    from simplepyq import SimplePyQ

    def process_data(args):
        print(f"Processing {args['data']}")

    scheduler = SimplePyQ("tasks.db")
    scheduler.add_channel("data", process_data)
    scheduler.enqueue("data", {"data": "item1"})
    scheduler.enqueue("data", {"data": "item2"})
    scheduler.run_until_complete()  # Blocks until all tasks are done

**Explanation**: `run_until_complete` processes all tasks and stops the scheduler, ideal for scripts or batch processing.

Testing
-------

To run the included unit tests:

.. code-block:: bash

    python -m unittest discover -s tests

This executes all tests in the `tests/` directory, covering task execution, retries, delays, and task management.

License
-------

Licensed under the Apache License 2.0. See the `LICENSE <LICENSE>`_ file for details.

----

**SimplePyQ** is a project powered by |caos|_.

.. |caos| replace:: **The California Open Source Company**
.. _caos: https://californiaopensource.com?utm_source=github&utm_medium=referral&utm_campaign=simplepyq_readme