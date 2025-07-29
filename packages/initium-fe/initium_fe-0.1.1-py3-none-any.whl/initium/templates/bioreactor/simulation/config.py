"""
Simulation configuration for bioreactor system
"""
import numpy as np

class SimulationConfig:
    def __init__(self, config):
        """
        Initialize simulation configuration
        """
        # Reactor parameters
        self.volume = config.get('reactor', {}).get('volume', 5.0)  # liters
        self.max_volume = config.get('reactor', {}).get('max_volume', 10.0)
        
        # Process parameters
        self.temperature = config.get('reactor', {}).get('temp', 37.0)  # °C
        self.ph = config.get('reactor', {}).get('ph', 7.2)
        self.agitation = config.get('reactor', {}).get('agitation', 200)  # RPM
        
        # Microorganism parameters
        self.inoculum_size = config.get('microorganism', {}).get('inoculum_size', 0.1)  # OD600
        self.growth_rate = config.get('microorganism', {}).get('growth_rate', 0.2)  # 1/h
        self.max_biomass = config.get('microorganism', {}).get('max_biomass', 10.0)  # OD600
        
        # Simulation parameters
        self.time_step = config.get('simulation', {}).get('time_step', 0.1)  # hours
        self.total_time = config.get('simulation', {}).get('total_time', 24)  # hours
        
        # Noise parameters for simulation realism
        self.temperature_noise = config.get('noise', {}).get('temperature', 0.5)
        self.ph_noise = config.get('noise', {}).get('ph', 0.1)
        self.do_noise = config.get('noise', {}).get('do', 1.0)
        
        # Process dynamics
        self.temperature_dynamics = config.get('dynamics', {}).get('temperature', 0.1)
        self.ph_dynamics = config.get('dynamics', {}).get('ph', 0.05)
        self.do_dynamics = config.get('dynamics', {}).get('do', 0.02)
        
    def get_initial_conditions(self):
        """
        Get initial conditions for simulation
        """
        return {
            'time': 0,
            'biomass': self.inoculum_size,
            'temperature': self.temperature + np.random.normal(0, self.temperature_noise),
            'ph': self.ph + np.random.normal(0, self.ph_noise),
            'do': 30.0 + np.random.normal(0, self.do_noise),
        }
