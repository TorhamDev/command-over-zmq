# ZMQ Async Command Runner

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![ZeroMQ](https://img.shields.io/badge/ZeroMQ-Async-grey.svg)](https://zeromq.org/)

## 📚 Table of Contents

- [About](#📝-about)
- [Features](#🚀-features)
- [Requirements](#📦-requirements)
- [How to Run](#🛠️-how-to-run)
- [Interview Notes](#🙋-interview-notes)
- [License](#license)

---

## 📝 About

This project is an **interview task** to demonstrate backend proficiency with asynchronous programming and message routing using **ZeroMQ** and **Python**.

The goal is to build a **command runner server** where clients can send shell commands, and workers execute them concurrently without blocking the system.

---

## 🚀 Features

- Asynchronous server with `asyncio` and `zmq.asyncio`
- ROUTER/DEALER (brokered) pattern for concurrency
- Subprocess command execution with structured JSON input/output
- Validation with `pydantic`
- Clean command-line client interface
- Timeout on commands

---

## 📦 Requirements

- Python 3.11+
- ZeroMQ
- Rich (for client output)
- aiofile
- pydantic

Install dependencies:

```bash
uv pip install .
```

## 🛠️ How to Run

### 1. Start the Server

```bash
git clone https://github.com/TorhamDev/command-over-zmq.git && cd command-over-zmq

python worker/main.py
```

This starts:

- A ROUTER/DEALER-based broker (with ZMQ request-reply behind it)

- At least one asynchronous worker that executes shell commands

### 2. Run the Client

Prepare a JSON file like this:

```json
{
  "command_type": "os",
  "command_name": "echo",
  "parameters": ["Hello, world!"]
}
```

Or multiple:

```json
[
  {
    "command_type": "shell",
    "command_name": "echo",
    "parameters": ["Hello, world!"]
  },
  {
    "command_type": "shell",
    "command_name": "sleep",
    "parameters": ["2"]
  }
]
```

Then run:

```bash

# -f is json file path and -a is server address
python client.py -f commands.json -a tcp://localhost:5555

```

use `client.py --help` to see help.

## 🙋 Interview Notes

This code was written as part of a timed technical interview task with limited scope. While functional and modular, it can be expanded with:

1- Job queuing & status tracking

2- Output streaming

3- Web UI or REST API interface

4- Testing using `pytest`

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
