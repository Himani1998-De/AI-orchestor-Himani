# AI-orchestor-Himani
Assignment submission

#### Trace for Assignment 3
TRACE | BOOTSTRAP | repo=mock_buggy_repo | source_files=3
TRACE | RAG | indexed_chunks=3 | retrieved_chunks=3 | injected_into_initial_state=yes
TRACE | CODER | attempt=1 | rag_chunks=3 | feedback_injected=no | wrote=generated_feature.py
TRACE | REVIEWER | attempt=1 | verdict=REJECTED | route=coder | feedback=REJECTED: missing required markers: from mock_buggy_repo.validation import normalize_email; normalized_email = normalize_email(email); return get_user_by_email(normalized_email)
TRACE | CODER | attempt=2 | rag_chunks=3 | feedback_injected=yes | wrote=generated_feature.py
TRACE | REVIEWER | attempt=2 | verdict=APPROVED | route=END | feedback=APPROVED: all guideline checks passed.
TRACE | FINAL | status=APPROVED | iterations=2/3 | generated=generated_feature.py

## Assignment 4
Rules - 
1. Preserve existing public interfaces unless the feature explicitly requires a change.
2. Follow existing module structure, naming, and import conventions.
3. Add type hints and docstrings for public interfaces.
4. Validate external inputs and provide actionable error messages.
5. Do not introduce secrets, hard-coded credentials, or unnecessary network calls.
6. Avoid global mutable state and keep functions cohesive.
7. Do not modify files outside the declared implementation target.

Install chromadb, fastmcp, langsmith, and openai in the same Python environment.
Set OPENAI_API_KEY and LANGSMITH_API_KEY.
Optionally set OPENAI_MODEL, LANGSMITH_PROJECT, and LANGSMITH_PROJECT_URL.
Run the script with a repository path and plain-language feature request, for example: python autonomous-engineering-pipeline.py --repo mock_buggy_repo --feature "Add input validation to the user registration workflow".

#### Component 1 — Codebase RAG Memory (Week 3)
The code implements Codebase RAG Memory using:

ChromaDB with persistent storage under .chroma.
AST parsing to index Python functions and classes.
Retrieval of the top three relevant symbols for each feature request.
Injection of the retrieved content into the Coder prompt as codebase_context.

One limitation: it rebuilds the Chroma collection on every run rather than incrementally updating it, and it indexes only Python functions/classes

 #### Component 2 — IDE MCP Server (Week 2)

Coder writes output through MCP - stage_candidate() calls write_file
Reviewer reads candidate through MCP - reviewer_node() calls read_file
File discovery - list_files
Compilation and Git actions - execute_code

#### Component 3 — Multi-Agent Coder/Reviewer (Week 3)
The core routing is implemented in run_pipeline()
It has a multi-agent Coder/Reviewer workflow:

1. Coder agent: coder() generates the requested Python implementation using the feature request, retrieved codebase_context, and any previous reviewer feedback.
2. Reviewer agent: reviewer() evaluates the candidate against architecture_guidelines.md and returns APPROVED or REJECTED.
3. MCP-mediated handoff: The Coder’s candidate is staged through write_file; the Reviewer reads it through read_file.
4. Feedback loop: Rejected candidates are deleted from staging, reviewer feedback is passed back to the Coder, and the Coder retries.
5. Maximum retries: The loop allows up to three attempts.
6. Graceful degrader: After three rejections, the pipeline ends with DEGRADED and does not save the candidate as a final source file.

#### Component 4 — HITL Commit Gate and Observability (Week 4)

It has both HITL Commit Gate and Observability.
HITL Commit Gate
Implemented through approval_node():
Displays the feature request.
Displays the Coder’s summary.
Displays the target file path.
Displays the first 30 lines of the staged code.
Requires the human to type APPROVE.
Saves the final file only after approval.
Performs Git staging and commit only after approval.
Deletes the staged candidate afterward.
If rejected, it returns HUMAN_REJECTED and does not create the final feature file.

The candidate is staged under .autopilot_staging/, so the Reviewer can inspect it without exposing an unapproved final file.
Observability
Implemented through:
@traceable decorators across:
Pipeline execution
RAG indexing and retrieval
Coder and Reviewer agents
MCP tool calls
HITL approval
Final save and commit
Graceful degradation
Token-log persistence

Local token_log.json containing one record per pipeline run, including:

Run ID
Timestamp
Feature request
Pipeline status
Rejection count
Input tokens
Output tokens
Total tokens
LangSmith project URL
Failure or commit details


## Final console output prints:

Total tokens consumed
LangSmith project URL

Important caveat
The implementation has an observability gap: token usage is explicitly captured only for the Coder and Reviewer LLM calls. If additional LLM calls are added later, their usage must also be aggregated into the run-level totals.
Also, langsmith_project_url() can return an unavailable message if project metadata cannot be retrieved. Setting LANGSMITH_PROJECT_URL explicitly would make the final output more relia
 
