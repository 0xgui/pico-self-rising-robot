import argparse
import time

import mujoco
import mujoco.viewer
from stable_baselines3 import PPO

from robo1_env import DEFAULT_FALLEN_POSES, Robo1GetupEnv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pose", choices=DEFAULT_FALLEN_POSES, default=None)
    parser.add_argument("--studio", action="store_true", help="open a clean, close-up view for recording")
    args = parser.parse_args()

    fallen_poses = (args.pose,) if args.pose is not None else DEFAULT_FALLEN_POSES
    env = Robo1GetupEnv("robo1.xml", fallen_poses=fallen_poses)
    model = PPO.load("robo1_getup_ppo", device="cpu")
    reset_options = {"pose": args.pose} if args.pose is not None else None
    obs, info = env.reset(options=reset_options)
    print("initial pose:", info["pose"])

    with mujoco.viewer.launch_passive(
        env.model,
        env.data,
        show_left_ui=not args.studio,
        show_right_ui=not args.studio,
    ) as viewer:
        if args.studio:
            with viewer.lock():
                viewer.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
                viewer.cam.lookat[:] = [env.data.qpos[0] + 0.08, env.data.qpos[1] - 0.08, 0.14]
                viewer.cam.distance = 0.42
                viewer.cam.azimuth = 135
                viewer.cam.elevation = -25
        while viewer.is_running():
            action, _ = model.predict(obs, deterministic=True)
            obs, _, terminated, truncated, _ = env.step(action)
            if args.studio:
                with viewer.lock():
                    viewer.cam.lookat[0] += 0.08 * (env.data.qpos[0] + 0.08 - viewer.cam.lookat[0])
                    viewer.cam.lookat[1] += 0.08 * (env.data.qpos[1] - 0.08 - viewer.cam.lookat[1])
            viewer.sync()
            time.sleep(env.model.opt.timestep * env.frame_skip)
            if terminated or truncated:
                obs, info = env.reset(options=reset_options)
                print("initial pose:", info["pose"])


if __name__ == "__main__":
    main()
