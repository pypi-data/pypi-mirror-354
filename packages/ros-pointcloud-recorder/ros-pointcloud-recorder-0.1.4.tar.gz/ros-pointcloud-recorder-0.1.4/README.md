# ROS PointCloud Recorder

一个简单的Python库，用于录制ROS点云话题并导出为PCD文件。

**Github地址：[https://github.com/Knighthood2001/ros-pointcloud-recorder](https://github.com/Knighthood2001/ros-pointcloud-recorder)**

## 依赖
重点说明：安装这个项目包的时候，我没有指定需要安装`pcl-ros`和`rosbag`，但是你在使用的时候，是需要有这个包的，因为这两个包，一般都是通过`apt install ros-<ros版本>-pcl-ros`和`apt install ros-<ros版本>-rosbag`安装的，所以你需要先安装这两个包。

- **ROS (必须安装`rosbag`和`pcl_ros`)**，因此你需要先安装ROS环境，才能使用ros-pointcloud-recorder。
- Python 3.6+

## 安装

```bash
pip install ros-pointcloud-recorder
```
## 快速开始

```python
from ros_pointcloud_recorder import PointCloudRecorder
# 创建录制器
recorder = PointCloudRecorder(
    topics=['/points_raw1', '/points_raw2'],
    output_dir='./data',
    recording_duration=2.0
)

# 执行录制并导出
pcd_paths = recorder.record_and_export()

print("导出完成:")
for topic, path in pcd_paths.items():
    print(f"{topic} -> {path}")
```

## 高级功能

- 自定义导出路径
- 单独控制录制和导出流程
- 自定义日志配置
- 保留中间bag文件

**详细用法请参考[示例代码](examples/)。**


## 设计要点

1. **模块化设计**：将功能分解为可独立调用的方法
2. **灵活性**：支持自定义路径、录制时长等参数
3. **健壮性**：完善的错误处理和日志记录
4. **易用性**：提供简单的一键录制导出方法
5. **可扩展性**：设计良好的API便于未来扩展功能

通过这种封装，用户只需简单的几行代码就可以实现点云录制功能，同时保留了高级用户需要的灵活性。

## 更新日志

- **v0.1.0** (2025-06-10)
  - 初始发布，提供基本的点云录制和导出功能
- **v0.1.1** (2025-06-10)
  - 修改了README.md
- **v0.1.2** (2025-06-10)
  - 修改了requirements.txt
- **v0.1.3** (2025-06-10)
  - 修改了README.md 
  - 修改了setup.py
- **v0.1.4** (2025-06-10)
  - 支持自定义bag文件名称
  - 完善了README.md