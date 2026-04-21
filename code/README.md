# pico_interface_pkg

This package includes the code for both the node that needs to run on the Latte Panda to communicate with the pico as well as the code that needs to be flashed onto the pico.

The code on the pico itself has a simple overall function. It will poll its serial port, take in a message, and then decode that message and exectute an action based on its contents.


## starting

```bash
ros2 run pico_interface_pkg pico_host_node
```

## pico_science_node.py - (All Pico Code For Deimos)

Commands to run Linear Actuator on Manipulator

extend
```bash
ros2 topic pub --once /science/actuator_pos robot_interfaces/msg/STargetedFloat "{target: 'act', data: 1.0}"
```

retract
```bash
ros2 topic pub --once /science/actuator_pos robot_interfaces/msg/STargetedFloat "{target: 'act', data: 0.0}"
```

stop
```bash
ros2 topic pub --once /science/actuator_pos robot_interfaces/msg/STargetedFloat "{target: 'act', data: 0.5}"
```

