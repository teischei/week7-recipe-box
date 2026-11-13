# Concurrent agent notes

## Tasks

I used Shopping List and Tag Filter for the parallel part of the assignment. The tasks were independent at the feature level, but both agents needed to update `main.py` and `test_main.py`.

## Worktree setup

I started from the main checkout in `week7-recipe-box` and created two worktrees.

```bash
git worktree add ../recipe-task-a -b task-a
git worktree add ../recipe-task-b -b task-b
```

The Shopping List agent worked only in `../recipe-task-a` on `task-a`. The Tag Filter agent worked only in `../recipe-task-b` on `task-b`. They both received one implementation prompt and ran their own tests without committing or pushing.

## Collision risk and supervision

The main risk was that both agents changed the same two files. Separate worktrees kept one agent from seeing or overwriting the other agent's uncommitted changes. I reviewed the diffs after both agents finished, committed each task on its own branch, and merged the branches into main one at a time. Git merged the changes automatically, and I then ran the combined test suite. The result was 6 passing tests before I started the generator and critic task.

## Branch evidence

- Shopping List implementation commit [`0720370`](https://github.com/teischei/week7-recipe-box/commit/0720370)
- Tag Filter implementation commit [`c07b56c`](https://github.com/teischei/week7-recipe-box/commit/c07b56c)
