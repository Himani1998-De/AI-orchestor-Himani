# Week 2 Assignment - Validated MCP Tools and Bounded Podman Execution

Build a Safe Local Agent Capability Service

### What to Build

Build one Python application with two connected capabilities:

1. A typed, validated file workspace exposed through FastMCP.
2. A Podman code runner that executes supplied Python source in a short-lived, restricted container.

The file service demonstrates how an agent receives permitted capabilities. The sandbox demonstrates how generated code can run without inheriting unrestricted host access. The two capabilities must share clear validation, structured results, and observable failures.

python -m pip install "fastmcp>=2,<3" "pydantic>=2,<3" "podman>=5" pytest

python validated_file_service.py --explore
python podman_code_runner.py --demo

podman run --rm student-sandbox-app:latest

python -m pytest -q
