# -*- coding: utf-8 -*-
"""
    RAISE - RAI Certified Node API

    @author: Mikel Hernández Jiménez - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

PYTHON_3_8_DOCKERFILE_TEMPLATE = """FROM python:3.8
COPY ./ /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_9_DOCKERFILE_TEMPLATE = """FROM python:3.9
COPY ./ /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_10_DOCKERFILE_TEMPLATE = """FROM python:3.10
COPY ./ /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_11_DOCKERFILE_TEMPLATE = """FROM python:3.11
COPY ./ /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_12_DOCKERFILE_TEMPLATE = """FROM python:3.12
COPY ./ /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""
