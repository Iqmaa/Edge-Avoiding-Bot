## Edge Avoiding Bot

<img width="1392" alt="image" src="/Media/bot1.png"/>

A bot that use  LIDAR to determine the edge of a table and move around it while avoiding those edges

## Steps to run Locally

1. Clone the repo

2. source the workspace
```
colcon build --symlink-install
```

3. set up the workspace
```
source install/setup.bash
```

4. run the following in terminal
```
ros2 launch bot_bringup simulated_robot.launch.py
```

- open another terminal to run this
```
ros2 run bot_script edge_detection
```

[Botvid.webm](https://github.com/user-attachments/assets/ff373cac-db30-4ac0-ae30-e43cb04a1c11)

