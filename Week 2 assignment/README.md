# Week 2 Assignment - Validated MCP Tools and Bounded Podman Execution

Build a Safe Local Agent Capability Service

### What to Build

Build one Python application with two connected capabilities:

1. A typed, validated file workspace exposed through FastMCP.
2. A Podman code runner that executes supplied Python source in a short-lived, restricted container.

The file service demonstrates how an agent receives permitted capabilities. The sandbox demonstrates how generated code can run without inheriting unrestricted host access. The two capabilities must share clear validation, structured results, and observable failures.
