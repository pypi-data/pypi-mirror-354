"""
PID Controller implementation for bioreactor control system
"""
import numpy as np

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0
        self.max_integral = 1000
        self.sample_time = 1.0  # seconds
        
    def update(self, current_value, dt=None):
        """
        Calculate PID output value for given reference feedback
        
        Args:
            current_value: Current process value
            dt: Time difference since last update
        
        Returns:
            float: PID output
        """
        if dt is None:
            dt = self.sample_time
            
        error = self.setpoint - current_value
        
        # Proportional term
        P = self.Kp * error
        
        # Integral term
        self.integral += error * dt
        self.integral = max(min(self.integral, self.max_integral), -self.max_integral)
        I = self.Ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / dt
        D = self.Kd * derivative
        
        # Update previous error
        self.previous_error = error
        
        # Calculate output
        output = P + I + D
        
        # Saturate output if needed
        return max(min(output, 100), -100)

class BioreactorController:
    def __init__(self, config):
        """
        Initialize bioreactor controller with multiple PID controllers
        """
        self.temperature_pid = PIDController(
            Kp=config.get('temperature', {}).get('Kp', 1.0),
            Ki=config.get('temperature', {}).get('Ki', 0.1),
            Kd=config.get('temperature', {}).get('Kd', 0.01),
            setpoint=config.get('temperature', {}).get('setpoint', 37.0)
        )
        
        self.ph_pid = PIDController(
            Kp=config.get('ph', {}).get('Kp', 1.0),
            Ki=config.get('ph', {}).get('Ki', 0.1),
            Kd=config.get('ph', {}).get('Kd', 0.01),
            setpoint=config.get('ph', {}).get('setpoint', 7.2)
        )
        
        self.do_pid = PIDController(
            Kp=config.get('do', {}).get('Kp', 1.0),
            Ki=config.get('do', {}).get('Ki', 0.1),
            Kd=config.get('do', {}).get('Kd', 0.01),
            setpoint=config.get('do', {}).get('setpoint', 30.0)
        )
        
    def update(self, measurements, dt):
        """
        Update all controllers with new measurements
        """
        return {
            'temperature': self.temperature_pid.update(measurements['temperature'], dt),
            'ph': self.ph_pid.update(measurements['ph'], dt),
            'do': self.do_pid.update(measurements['do'], dt)
        }
