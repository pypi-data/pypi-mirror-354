#!/usr/bin/env python3
import time
import math
from smbus import SMBus

MPU_ADDR = 0x68          # 根据AD0引脚调整
I2C_BUS = 3              # I2C-3接口
ACCEL_RANGE = 0x00       # ±2g
GYRO_RANGE = 0x18        # ±2000°/s
SAMPLING_RATE = 100      # 100Hz

# DMP固件数据（示例数据，需根据传感器型号调整）
DMP_FIRMWARE = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    # 此处省略实际固件数据（需从官方获取）
]

class MPU6500:
    def __init__(self):
        self.bus = SMBus(I2C_BUS)
        self.registers = {
            'PWR_MGMT_1': 0x6B,
            'GYRO_CFG': 0x1B,
            'ACCEL_CFG': 0x1C,
            'SMPLRT_DIV': 0x19,
            'USER_CTRL': 0x6A,
            'FIFO_EN': 0x23,
            'FIFO_COUNT_H': 0x72,
            'FIFO_R_W': 0x74,
            'DMP_CFG_1': 0x70,
            'DMP_CFG_2': 0x71,
            'WHO_AM_I': 0x75
        }
        
        self.gyro_scale = self._get_gyro_scale(GYRO_RANGE)
        self.accel_scale = self._get_accel_scale(ACCEL_RANGE)
        self._initialize_hardware()
#        self._load_dmp_firmware()
        self._configure_dmp()
    
    def _initialize_hardware(self):
        """初始化硬件寄存器"""
        self._write_reg('PWR_MGMT_1', 0x80)  # 软复位
        time.sleep(0.1)
        self._write_reg('PWR_MGMT_1', 0x01)  # 唤醒，选择陀螺仪X轴时钟
        time.sleep(0.1)
        
        self._write_reg('GYRO_CFG', GYRO_RANGE)
        self._write_reg('ACCEL_CFG', ACCEL_RANGE)
        self._write_reg('SMPLRT_DIV', (1000 // SAMPLING_RATE) - 1)
    
    def _load_dmp_firmware(self):
        """加载DMP固件（示例，需替换为实际固件）"""
        print("加载DMP固件...")
        for addr, data in enumerate(DMP_FIRMWARE):
            self._write_reg(0x40 + addr, data)  # 固件从0x40地址开始写入
            time.sleep(0.001)
        print("固件加载完成")
    
    def _configure_dmp(self):
        """配置DMP参数"""
        self._write_reg('USER_CTRL', 0x00)  # 禁用DMP
        self._write_reg('FIFO_EN', 0x00)    # 禁用FIFO
        self._write_reg('DMP_CFG_1', 0x03)  # 设置DMP采样率
        self._write_reg('DMP_CFG_2', 0x00)  # 禁用低功耗模式
        
        self._write_reg('USER_CTRL', 0x10)  # 复位FIFO
        time.sleep(0.01)
        self._write_reg('USER_CTRL', 0x80)  # 启用DMP
        time.sleep(0.1)
        self._write_reg('FIFO_EN', 0x40)    # 启用四元数FIFO
    
    def _write_reg(self, reg, value):
        """安全写入寄存器（支持寄存器名称字符串或数值地址）"""
        if isinstance(reg, str):
            reg_addr = self.registers[reg]
        else:
            reg_addr = reg
            
        try:
            self.bus.write_byte_data(MPU_ADDR, reg_addr, value)
        except Exception as e:
            print(f"写入寄存器0x{reg_addr:02X}失败: {e}")
    
    def read_dmp_quaternion(self):
        """读取DMP生成的四元数"""
        high = self.bus.read_byte_data(MPU_ADDR, self.registers['FIFO_COUNT_H'])
        low = self.bus.read_byte_data(MPU_ADDR, self.registers['FIFO_COUNT_H'] + 1)
        fifo_len = (high << 8) | low
        
        if fifo_len < 8:
            return None
        
        data = self.bus.read_i2c_block_data(MPU_ADDR, self.registers['FIFO_R_W'], 8)
        return self._parse_quaternion(data)
    
    def _parse_quaternion(self, bytes):
        """解析四元数（小端模式）"""
        q1 = self._bytes_to_sint16(bytes[0:2]) / 32768.0
        q2 = self._bytes_to_sint16(bytes[2:4]) / 32768.0
        q3 = self._bytes_to_sint16(bytes[4:6]) / 32768.0
        q4 = self._bytes_to_sint16(bytes[6:8]) / 32768.0
        return (q1, q2, q3, q4)
    
    def _bytes_to_sint16(self, bytes):
        val = (bytes[1] << 8) | bytes[0]
        return val if val < 32768 else val - 65536
    
    def _get_gyro_scale(self, range_bits):
        return {0x18: 16.4}[range_bits]
    
    def _get_accel_scale(self, range_bits):
        return {0x00: 16384.0}[range_bits]

if __name__ == "__main__":
    mpu = MPU6500()
    print("开始读取DMP数据...")
    
    try:
        while True:
            q = mpu.read_dmp_quaternion()
            if q:
                norm = math.sqrt(sum(x**2 for x in q))
                if norm > 0.5:  # 仅输出有效四元数
                    print(f"四元数: {q}, 模长: {norm}")
                else:
                    print("警告：四元数无效，模长过低")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("程序停止")