import pybullet as p
import pybullet_data
import time

# 连接 Pybullet 并设置模拟环境
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 加载地面、机器人和对象
p.loadURDF("plane.urdf")
robot = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0])
cube = p.loadURDF("cube_small.urdf", [0.5, 0, 0.5])

# 将机器人的关节设置到起始位置
for joint in range(p.getNumJoints(robot)):
    p.resetJointState(robot, joint, 0)

# 设置目标位置
target_position = [0.5, 0.5, 10]

# 模拟循环
for _ in range(10000):
    # 获取立方体的当前位置
    cube_pos, _ = p.getBasePositionAndOrientation(cube)

    # 计算立方体到目标位置的距离
    error = [(t - c) for t, c in zip(target_position, cube_pos)]

    # 为每个关节设置一个简单的控制命令，使立方体移动到目标位置
    for joint in range(p.getNumJoints(robot)):
        p.setJointMotorControl2(robot, joint, p.POSITION_CONTROL, targetPosition=error[2])

    # 步进模拟
    p.stepSimulation()
    
    # 延时以便于观察模拟
    time.sleep(0.01)

# 断开 Pybullet 连接
p.disconnect()
