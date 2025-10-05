# uni-notes Contribution Guide

Quick guide on contributring to `uni-notes`.

## Table Of Contents

- [uni-notes Contribution Guide](#uni-notes-contribution-guide)
  - [Table Of Contents](#table-of-contents)
    - [Filing Issues](#filing-issues)
    - [Making Pull Requests](#making-pull-requests)
    - [Reminders](#reminders)

### Filing Issues

- Don't remember how to file an issue on GitHub? Read the [GitHub Docs on creating an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).
- Search for any existing issues before opening a new one.
- Include your working environment in (OS, setup, application version).
- Describe expected vs. actual behavior.
- Add labels (e.g., `bug`, `enhancement`) and attach screenshots/logs if helpful.

### Making Pull Requests

- Don't remember how to make a PR on GitHub? Read the [GitHub Docs on creating a pull request](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).

1) **Branch naming**

~~~bash
git checkout -b feature/section-description
~~~

- Prefix with your tracker ticket if applicable (e.g., `feature/frontend-update-homepage`).

2) **Commit messages** (Conventional Commits)

~~~text
feat: add new notes to sysc-4810
fix: correct spelling error in README
chore: run markdown lint over repo
~~~

3) **Open a PR**

- Target `main`.
- Clearly describe what changed and why; link the issue/ticket.
- Include before/after screenshots for report changes.
- Request reviewers and add labels.

### Reminders

- Please be nice, or you'll make me sad (and I'll reject your PR and implement your suggestion myself >:D )
- Do **NOT** share answers to assignments/labs/midterms/exams in your PR,  that's an auto-reject.
