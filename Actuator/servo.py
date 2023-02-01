import RPi.GPIO as GPIO
import time


class MyServo:
	def __init__(self, sensor_port, PWM_frequency):
    #initialize the sensor
		self.sensor_port = sensor_port
		self.PWM_frequency = PWM_frequency 

	def set_angle(self, target_angle, smooth_step):

		# Set up the GPIO pin for the servo

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.sensor_port, GPIO.OUT)

		# Create a PWM instance for the servo
		servo = GPIO.PWM(self.sensor_port, self.PWM_frequency)
		servo.start(7.5)
		# Define the rotation range for the servo

		# Define the speed of the rotation
		def range_with_floats(start, stop, step):
			while stop > start:
				yield start
				start += step

		try:
			while True:
				# Increase the servo angle by the step value
				# for angle in range_with_floats(min_angle, max_angle, step):
				# 	servo.ChangeDutyCycle(angle)
				# 	time.sleep(0.01)

				for angle in range_with_floats(0, target_angle, smooth_step):
					servo.ChangeDutyCycle(angle)
					time.sleep(0.01)

		except KeyboardInterrupt:
			# Clean up the GPIO pins when the program is interrupted
			servo.stop()
			GPIO.cleanup()



# mySer = MyServo(13,50)
# mySer.set_angle(8,0.1)