# Asana Tasker

A simple Python utility to create tasks in Asana using their API.

## Installation

```bash
pip install asana-tasker
```

## Usage

```python
from asana_tasker.asana_task import create_asana_task

create_asana_task("your_token", "project_id", "New Task", "Some notes", "someone@example.com", "workspace_id")
```
