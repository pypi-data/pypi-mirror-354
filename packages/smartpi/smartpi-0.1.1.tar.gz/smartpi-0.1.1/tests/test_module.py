import sys
import time
from pathlib import Path

src_path = str(Path(__file__).resolve().parent.parent / "src")
sys.path.insert(0, src_path)


from smartpi.module import Uart3_funtions, base_driver
from smartpi.app_module import app_funtion


if __name__ == "__main__":
    ser = base_driver.uart3_init()
    if ser:
        try:
#            Uart3_funtions.boot_update()
#            Uart3_funtions.read_device_model()
#            Uart3_funtions.read_version()
#            Uart3_funtions.read_factory_data()
#            Uart3_funtions.read_hardware_ID()
#            Uart3_funtions.read_device_name()
#            Uart3_funtions.write_device_name("Martin")
#            Uart3_funtions.read_connected()
#            Uart3_funtions.read_battery()
#            Uart3_funtions.read_peripheral()

            
            while True:
                  app_funtion.write_motor_dir(1,0)
                  app_funtion.write_motor_speed(1,100)
                  time.sleep(0.5)
                  app_funtion.write_motor_dir(1,1)
                  app_funtion.write_motor_speed(1,50)
                  time.sleep(0.5)
#                  app_funtion.servo_operate(1,1,0)                  
#                  time.sleep(0.5)
#                  app_funtion.servo_operate(1,1,180)
#                  time.sleep(0.5)           


        except KeyboardInterrupt:
            print("\n程序终止")
        finally:
            ser.close()
            print("串口关闭")
            
            