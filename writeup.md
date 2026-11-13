# Week 7 Writeup

## Concurrent agents

For the parallel section, I chose the Shopping List and Tag Filter tasks. I created two git worktrees named `recipe-task-a` and `recipe-task-b` with their own branches. Each agent only worked in its assigned worktree and was allowed to edit the feature code and tests, run pytest, and report its changes. I did not allow either agent to commit, push, edit documentation, or touch the other worktree. Both tasks changed `main.py` and `test_main.py`, so the main risk was a merge collision. Keeping the worktrees separate protected the uncommitted work, and I reviewed the diffs, committed both branches, merged them one at a time, and ran the combined test suite. The combined result was 6 passing tests.

## Generator critic loop

I used Ingredient Scaling for the generator and critic loop. The generator made the first version of the scaled recipe endpoint and tests. The critic reviewed correctness, tests, and clarity. In the first round, it found that zero and negative factors should be rejected and that the test should show the ID and tags are kept. The generator made those changes and added a zero-factor test. In the second round, the critic noticed that the endpoint accepts float factors but only had a whole-number test. The generator added a test that scales `200 g flour` by `0.5` to `100 g flour`. The final critic review signed off after the full test suite passed with 10 tests. The detailed prompts, reviews, and revision rounds are in [the generator critic transcript](docs/orchestration/generator-critic-transcript.md).

## Autonomy and supervision

I gave the implementation agents limited autonomy. They could write code and tests inside one assigned worktree and run tests, but they could not commit, push, or change project documentation. The critic agents had read-only autonomy and gave feedback using the same short rubric. I supervised by checking the diffs, reviewing the test results, making the commits after each major step, and running the combined test suite after merges.

## What I learned

Running agents in separate worktrees made the parallel work easier to manage because their unfinished changes could not overwrite each other. I still needed to watch for collisions because independent tasks can use the same files. The generator and critic loop helped find missing validation and test coverage that the first implementation missed. I am more comfortable giving agents limited autonomy when I can review the diff and verify the result with tests before I merge it.
