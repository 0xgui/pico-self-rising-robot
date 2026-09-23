# My experiment plans

Plans for changes I want to try on my build of [HomeMadeGarbage's SelfRisingRobot](https://github.com/homemadegarbage/SelfRisingRobot). Each file is a proposal; no result or speedup is claimed until it is measured.

| Plan | Goal | Status |
|------|------|--------|
| [pufferlib-migration.md](pufferlib-migration.md) | Speed up training by replacing SB3's vectorization/PPO with PufferLib, keeping CPU MuJoCo as-is | Not started |
| [led-status-indicator.md](led-status-indicator.md) | Use the ATOM Matrix's built-in LED grid to show robot state (fallen/getting up/upright/aborted) without needing the web UI | Not started |

## Future (not yet planned in detail)

- **MJX + `mujoco_playground` migration** — rewrite `robo1_env.py` to run on GPU via MuJoCo MJX,
  enabling thousands of parallel envs instead of dozens. Bigger lift (env logic must become
  JAX-traceable, no Python branching). Makes the most sense once training throughput itself
  (not raw wall-clock) is the limiting factor — e.g. once we want heavy domain randomization
  (servo friction/damping, IMU noise, mass) and need many envs to keep that fast.
