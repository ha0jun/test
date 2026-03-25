# Research Workflow (Haojun + Chako)

This repository follows the rules below.

## 1) Research diary

- Keep a research diary in `diary/`.
- Each diary filename starts with timestamp + high-level summary.
- Use **PST/PDT (America/Los_Angeles)** for diary timestamps.
- Format example: `2026-3-24-13:00-build-gui.md`
- Start a new diary file whenever there is a substantial improvement.

## 2) Code quality and structure

- Write clean, structured, abstracted code.
- Split code into separate Python files with clear grouping by responsibility.
- Target file size: roughly **200–1000 lines** per file when reasonable.

## 3) Branching + iteration process

- Chako uses branch: `chako`.
- Iterate and commit regularly on `chako`.
- After every **10 commits since the last feedback checkpoint**, report progress and stop for feedback.
- Submit a PR and ask Haojun for feedback before continuing.
