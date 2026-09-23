# Plan: Migrate training from SB3 to PufferLib

## Goal

Speed up `RL/train_robo1.py` by replacing Stable-Baselines3's vectorization
(`SubprocVecEnv`) and PPO trainer with PufferLib's, while keeping MuJoCo (CPU) and
`robo1_env.py`'s physics/reward/reset logic completely unchanged. This is the
low-effort speed option — no JAX rewrite, no GPU physics. See `README.md` in this
folder for the higher-ceiling/higher-effort alternative (MJX).

## Why

- PufferLib's emulation layer wraps existing Gymnasium environments with ~1 line
  of code — `Robo1GetupEnv` doesn't need to change.
- PufferLib's vectorization may reduce per-step Python/IPC overhead compared with
  SB3's `SubprocVecEnv`. The speed difference on this robot has not been measured.
- Ceiling is CPU-core-bound (same as today), not GPU-scale — that's fine for a
  2-DOF task and is why this is worth doing before considering MJX.

## Current training configuration (keep for a later comparison)

- `RL/train_robo1.py`: SB3 `PPO("MlpPolicy", ...)`, `SubprocVecEnv`, `N_ENVS = 6`,
  `n_steps=512`, `batch_size=256`, `learning_rate=3e-4`, `gamma=0.99`, `device="cpu"`.
- `RL/export_policy_header.py` loads the trained model via `PPO.load(...)` and reads
  `model.policy.state_dict()`, filtering keys containing `policy_net`/`action_net`
  (SB3's `MlpPolicy` naming convention) to build the C header.
- `RL/pretrain_robo1_from_scripted.py` produces the initial `robo1_getup_ppo.zip`
  (behavioral cloning) that PPO fine-tuning continues from — also SB3-format.

## Key risk to solve first: the export step is SB3-format-specific

`export_policy_header.py` hard-depends on SB3's checkpoint structure
(`PPO.load()` + `policy_net.N.weight`/`action_net.weight` key names). PufferLib
trains a plain PyTorch `nn.Module` with its own architecture/naming — it will
**not** produce a compatible `state_dict`. This must be addressed explicitly,
not discovered after training completes. Two options:

1. **Preferred:** Write a small, explicit MLP policy class for PufferLib training
   (matching the same architecture shape as today's `MlpPolicy`: same hidden
   layer sizes, tanh activations, 4-in/2-out) and add a new export function that
   reads *its* state dict layer names. Keep `export_policy_header.py`'s SB3 path
   working (for `pretrain_robo1_from_scripted.py`'s output) and add a
   `--source={sb3,puffer}` flag or a separate `export_policy_header_puffer.py`.
2. **Fallback:** After PufferLib training, manually copy the learned weight
   tensors into an SB3 `MlpPolicy` shell purely for export purposes. More
   fragile (relies on layer-order matching by hand) — only use if (1) proves
   awkward.

Decide between these during implementation, not before — depends on how
PufferLib's default MLP policy is structured once we look at it directly.

## Implementation steps

1. **Add dependency.** Add `pufferlib` to `RL/requirements.txt`. Install in the
   existing venv and confirm `import pufferlib` works with the existing
   `gymnasium`/`mujoco` versions already pinned (check for conflicts).

2. **New training script, don't overwrite the old one.** Create
   `RL/train_robo1_puffer.py` (leave `train_robo1.py` untouched as a fallback /
   comparison baseline). Wrap `Robo1GetupEnv` with PufferLib's emulation layer
   and set up PufferLib's vectorized env with `n_envs` matching the local CPU
   core count (replace the hardcoded `N_ENVS = 6`).

3. **Swap the trainer.** Replace SB3's `PPO(...)` / `model.learn(...)` with
   PufferLib's `PuffeRL` trainer. Match hyperparameters to the current baseline
   as closely as PufferLib's API allows (`n_steps=512`, `batch_size=256`,
   `learning_rate=3e-4`, `gamma=0.99`) so the comparison in step 6 isolates the
   orchestration speedup rather than confounding it with different learning
   dynamics.

4. **Resolve the export path** per the "Key risk" section above. Confirm
   `python export_policy_header.py --source=puffer ... -o policy_network.h`
   (or equivalent) produces a header with the same `OBS_DIM=4` / `ACTION_DIM=2`
   and plausible-looking weights.

5. **Keep behavioral cloning compatible.** Confirm whether
   `pretrain_robo1_from_scripted.py`'s output can still seed the new PufferLib
   training run, or whether pretraining needs its own PufferLib-side version.
   If not straightforward, it's acceptable short-term to train from scratch
   with PufferLib and revisit BC pretraining as a follow-up.

6. **Benchmark before/after.** Record steps/sec and wall-clock time to reach
   200K timesteps for both `train_robo1.py` (SB3 baseline) and
   `train_robo1_puffer.py`, run back-to-back on the same machine. This is the
   number that justifies (or kills) the migration.

7. **Validate the resulting policy, not just training speed.** Run
   `eval_robo1_policy.py` against the PufferLib-trained model (via whatever
   loading path step 4 established) and compare results across all 4 fallen
   poses with the original `robo1_getup_ppo.zip`. Flash the exported header
   to real hardware and compare getup behavior with the current build.

## Acceptance criteria

- [ ] Evaluate both the original SB3 model and the PufferLib-trained model on
      all 4 poses, recording their actual success rates and timestep budgets.
- [ ] Measured wall-clock time for both training paths is documented, whether
      PufferLib is faster or slower on this workload.
- [ ] `policy_network.h` exported from the PufferLib-trained model runs
      correctly on the real robot (self-rights from all 4 fallen poses).
- [ ] `train_robo1.py` (SB3 path) still works unmodified, so this is additive,
      not a breaking migration.

## Out of scope for this plan

- GPU-native physics (MJX) — separate future plan, see this folder's `README.md`.
- Domain randomization / reward tuning — orthogonal to this change; do after,
  once whichever training path is faster is settled.
