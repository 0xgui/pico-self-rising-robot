# Original project's RL baseline

The simulation, training scripts, STL assets, and pretrained PPO model in this directory come from [HomeMadeGarbage's SelfRisingRobot](https://github.com/homemadegarbage/SelfRisingRobot). I include them as the baseline for my build and proposed experiments. The checked-in `robo1_getup_ppo.zip` is their pretrained model; this repository does not document a training run of my own.

## Files

Files needed to run this part of the repo:

- `robo1_getup_ppo.zip` - trained Stable-Baselines3 PPO model
- `robo1_env.py` - Gymnasium/MuJoCo environment
- `robo1.xml` - MuJoCo model definition
- `assets/` - STL meshes referenced by `robo1.xml`
- `play_robo1_policy.py` - play back the trained model
- `eval_robo1_policy.py` - evaluate from each fallen pose
- `search_all_getup.py` - search for candidate getup trajectories for each fallen pose and output a `BEST_SEQ` to feed into `getup_reference.py`
- `getup_reference.py` - servo target-angle waypoint sequences per fallen pose, used to generate training data
- `scripted_getup.py` - play back the getup trajectories defined in `getup_reference.py` in the MuJoCo viewer, for review
- `pretrain_robo1_from_scripted.py` - generate (observation, action) pairs from the `getup_reference.py` trajectories and pretrain the PPO policy via behavioral cloning
- `train_robo1.py` - additional PPO training
- `export_policy_header.py` - generate a C header for Arduino from the trained model
- `requirements.txt` - Python dependencies

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Play

```bash
python play_robo1_policy.py
```

To play back from a specific initial pose:

```bash
python play_robo1_policy.py --pose roll_pos
python play_robo1_policy.py --pose roll_neg
python play_robo1_policy.py --pose pitch_pos
python play_robo1_policy.py --pose pitch_neg
```

## Evaluate

```bash
python eval_robo1_policy.py
```

## Training

Pretrains an initial policy from the getup reference data defined in `getup_reference.py`.

To re-search for getup trajectories, run:

```bash
python search_all_getup.py
```

Take the resulting `BEST_SEQ` or `REFERENCE_CANDIDATES` array and feed it into
`getup_sequence_for_pose()` in `getup_reference.py`.

Pretrain an initial policy from the reference data:

```bash
python pretrain_robo1_from_scripted.py
```

This produces `robo1_getup_ppo.zip`.

Continue with additional PPO training:

```bash
python train_robo1.py --model-in robo1_getup_ppo.zip --timesteps 200000 --n-envs 6 --model-out robo1_getup_ppo
```

To train PPO from scratch instead, omit `--model-in`:

```bash
python train_robo1.py --timesteps 200000 --n-envs 6 --model-out robo1_getup_ppo
```

## Export for Arduino

Generates `policy_network.h` from the trained model.

```bash
python export_policy_header.py robo1_getup_ppo.zip -o policy_network.h
```

Place the generated `policy_network.h` alongside the Arduino sketch to use it.

## Notes

- `robo1_getup_ppo.zip` depends on the environment definitions in `robo1.xml` and `robo1_env.py`.
- The MuJoCo model can't be loaded without the STL files in `assets/`.
- Run everything from the repo root of this `RL/` directory.
