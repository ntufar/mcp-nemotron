# Tasks: MCP Server for LLM Directory and File Browsing

**Input**: Design documents from `/specs/001-feature-project-to-create-mcp-server-to-help-llm-to-browse/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/, quickstart.md

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB connections, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python 3.11 project with MCP SDK dependencies
- [X] T003 [P] Configure linting and formatting tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [X] T004 [P] Contract test for list_directory in tests/contract/test_list_directory.py
- [X] T005 [P] Contract test for read_file in tests/contract/test_read_file.py
- [X] T006 [P] Integration test directory listing scenario in tests/integration/test_directory_listing.py
- [X] T007 [P] Integration test file reading scenario in tests/integration/test_file_reading.py
- [X] T008 [P] Integration test access denied scenario in tests/integration/test_access_denied.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [X] T009 [P] Directory model in src/models/directory.py
- [X] T010 [P] File model in src/models/file.py
- [X] T011 FileSystemService in src/services/filesystem_service.py
- [X] T012 list_directory tool implementation
- [X] T013 read_file tool implementation
- [X] T014 Input validation
- [X] T015 Error handling and logging

## Phase 3.4: Integration
- [X] T016 Security middleware for access control
- [X] T017 Request/response logging
- [X] T018 MCP server configuration

## Phase 3.5: Polish
- [X] T019 [P] Unit tests for validation in tests/unit/test_validation.py
- [X] T020 Performance tests (<100ms)
- [X] T021 [P] Update docs/README.md
- [X] T022 Remove duplication
- [X] T023 Run quickstart.md

## Dependencies
- Tests (T004-T008) before implementation (T009-T015)
- Models (T009-T010) before services (T011)
- Services (T011) before tools (T012-T013)
- Implementation before integration (T016-T018)
- Everything before polish (T019-T023)

## Parallel Example
```
# Launch T004-T008 together:
Task: "Contract test for list_directory in tests/contract/test_list_directory.py"
Task: "Contract test for read_file in tests/contract/test_read_file.py"
Task: "Integration test directory listing scenario in tests/integration/test_directory_listing.py"
Task: "Integration test file reading scenario in tests/integration/test_file_reading.py"
Task: "Integration test access denied scenario in tests/integration/test_access_denied.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts