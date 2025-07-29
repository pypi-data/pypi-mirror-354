# ROS PointCloud Recorder

一个简单的Python库，用于录制ROS点云话题并导出为PCD文件。

## 安装

```bash
pip install ros-pointcloud-recorder
```
## 快速开始

```python
from ros_pointcloud_recorder import PointCloudRecorder
```
## 创建录制器
```python
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

详细用法请参考[示例代码](examples/)。

## 依赖

- ROS (必须安装`rosbag`和`pcl_ros`)
- Python 3.6+


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