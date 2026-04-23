# Project Initialization Directive

## Goal
Establish and maintain the 3-layer architecture as defined in `Agents.md`.

## Current State
- **Layer 1 (Directives)**: This directory has been initialized.
- **Layer 2 (Orchestration)**: AI Agent (Antigravity) is configured to use this structure.
- **Layer 3 (Execution)**: `execution/` directory is initialized. Existing legacy scripts reside in sub-modules (e.g., `skill-creator/scripts`, `seo-expert/scripts`).

## Tasks
1. [x] Create `directives/`, `execution/`, and `.tmp/` directories.
2. [x] Create `.gitignore` to protect sensitive and temporary files.
3. [x] Verify write permissions for the project root.
4. [ ] Consolidate or reference legacy scripts in `execution/`.
5. [ ] Define core project directives.

## Operating Procedures
- New deterministic logic must be placed in `execution/`.
- New SOPs must be placed in `directives/`.
- Use `.tmp/` for all intermediate data processing.
