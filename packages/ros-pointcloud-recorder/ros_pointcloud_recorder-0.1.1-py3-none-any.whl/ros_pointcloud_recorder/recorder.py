import subprocess
import time
import os
import signal
import logging
import shutil

class PointCloudRecorder:
    """ROS点云录制器，支持录制点云话题并导出为PCD文件"""
    
    def __init__(self, topics, output_dir="./", recording_duration=1.0, cleanup=True, logger=None):
        """
        初始化点云录制器
        
        参数:
            topics (list): 要录制的点云话题列表
            output_dir (str): 输出目录路径
            recording_duration (float): 录制时长(秒)
            cleanup (bool): 是否在导出后清理临时文件
            logger: 自定义日志记录器
        """
        if not topics:
            raise ValueError("至少需要一个录制话题")
        if recording_duration <= 0:
            raise ValueError("录制时长必须大于0")
        
        self.topics = topics
        self.output_dir = output_dir
        self.recording_duration = recording_duration
        self.cleanup = cleanup
        self.recording_process = None
        self.bag_file = "recorded_point_clouds.bag"
        
        # 配置日志
        self.logger = logger or logging.getLogger("PointCloudRecorder")
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        self.bag_file = os.path.join(self.output_dir, self.bag_file)
        
        self.logger.info(f"初始化录制器: 输出目录={self.output_dir}, 录制时长={self.recording_duration}s")
    
    def start_recording(self):
        """开始录制点云话题"""
        try:
            self.logger.info(f"开始录制话题: {', '.join(self.topics)}")
            self.recording_process = subprocess.Popen(
                ['rosbag', 'record', '-O', self.bag_file] + self.topics,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # 等待录制进程启动
            time.sleep(0.5)
            if self.recording_process.poll() is not None:
                stderr = self.recording_process.stderr.read().decode('utf-8')
                raise RuntimeError(f"录制进程启动失败: {stderr}")
            return True
        except Exception as e:
            self.logger.error(f"录制启动失败: {str(e)}")
            raise RuntimeError("录制启动失败") from e
    
    def stop_recording(self):
        """停止录制"""
        if self.recording_process and self.recording_process.poll() is None:
            try:
                # 发送SIGINT信号优雅停止录制
                self.recording_process.send_signal(signal.SIGINT)
                self.recording_process.wait(timeout=5)
                self.logger.info("录制已停止")
                return True
            except Exception as e:
                self.logger.error(f"停止录制失败: {str(e)}")
                return False
        return False
    
    def export_pcd(self, custom_paths=None):
        """
        导出PCD文件
        
        参数:
            custom_paths (dict): 自定义话题导出路径映射
             {topic: output_path}
        
        返回:
            dict: 导出的PCD文件路径 {topic: pcd_path}
        """
        pcd_paths = {}
        
        for topic in self.topics:
            # 确定输出目录
            if custom_paths and topic in custom_paths:
                output_dir = custom_paths[topic]
            else:
                # 默认输出目录：output_dir/topic_name
                topic_name = topic.replace('/', '_').lstrip('_')
                output_dir = os.path.join(self.output_dir, topic_name)
            
            # 确保目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            try:
                self.logger.info(f"导出话题 {topic} 到 {output_dir}")
                subprocess.run(
                    ['rosrun', 'pcl_ros', 'bag_to_pcd', self.bag_file, topic, output_dir],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                pcd_paths[topic] = output_dir
            except subprocess.CalledProcessError as e:
                self.logger.error(f"导出话题 {topic} 失败: {e.stderr.decode('utf-8')}")
                pcd_paths[topic] = None
        
        return pcd_paths
    
    def record_and_export(self, custom_paths=None):
        """
        完整流程：录制+导出
        
        参数:
            custom_paths (dict): 自定义话题导出路径映射
        
        返回:
            dict: 导出的PCD文件路径 {topic: pcd_path}
        """
        try:
            # 启动录制
            self.start_recording()
            
            # 等待录制时间
            self.logger.info(f"录制中... (时长: {self.recording_duration}s)")
            time.sleep(self.recording_duration)
            
            # 停止录制
            self.stop_recording()
            
            # 确保文件写入完成
            time.sleep(0.5)
            
            # 导出PCD
            return self.export_pcd(custom_paths)
        except Exception as e:
            self.logger.error(f"录制导出流程失败: {str(e)}")
            raise
        finally:
            # 清理临时文件
            if self.cleanup and os.path.exists(self.bag_file):
                os.remove(self.bag_file)
                self.logger.info(f"已清理临时文件: {self.bag_file}")