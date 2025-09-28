import hiwonder.ros_robot_controller_sdk as rrc
from hiwonder.Controller import Controller


board = rrc.Board()
ctl = Controller(board)

ctl.set_pwm_servo_pulse(1, 1700, 500)
ctl.set_pwm_servo_pulse(2, 1400, 500) 

# print(board.bus_servo_read_angle_limit(1))