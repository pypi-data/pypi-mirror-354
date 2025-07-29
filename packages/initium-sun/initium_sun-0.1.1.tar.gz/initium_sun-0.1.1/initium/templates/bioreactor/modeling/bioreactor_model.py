"""
Mathematical models for bioreactor dynamics
"""
import numpy as np
from scipy.integrate import odeint

class BioreactorModel:
    def __init__(self, config):
        """
        Initialize bioreactor mathematical model
        """
        self.config = config
        self.volume = config.get('reactor', {}).get('volume', 5.0)
        
    def growth_rate(self, biomass, temperature, ph, do):
        """
        Calculate specific growth rate using modified Monod kinetics
        """
        # Temperature effect
        T_opt = self.config.get('microorganism', {}).get('optimal_temp', 37.0)
        temperature_factor = np.exp(-((temperature - T_opt) / 5.0)**2)
        
        # pH effect
        pH_opt = self.config.get('microorganism', {}).get('optimal_ph', 7.2)
        pH_factor = np.exp(-((ph - pH_opt) / 0.5)**2)
        
        # DO effect
        do_min = self.config.get('microorganism', {}).get('min_do', 20.0)
        do_factor = do / (do_min + do)
        
        # Maximum growth rate
        mu_max = self.config.get('microorganism', {}).get('growth_rate', 0.2)
        
        return mu_max * temperature_factor * pH_factor * do_factor
    
    def mass_balance(self, y, t, u):
        """
        System of ODEs for bioreactor mass balance
        
        Args:
            y: State vector [biomass, temperature, ph, do]
            t: Time
            u: Control inputs [temp_control, ph_control, do_control]
        """
        biomass, temperature, ph, do = y
        temp_control, ph_control, do_control = u
        
        # Growth rate
        mu = self.growth_rate(biomass, temperature, ph, do)
        
        # Biomass dynamics
        dXdt = mu * biomass
        
        # Temperature dynamics
        dTdt = (temp_control - temperature) / self.config.get('dynamics', {}).get('temperature', 0.1)
        
        # pH dynamics
        dPhdt = (ph_control - ph) / self.config.get('dynamics', {}).get('ph', 0.05)
        
        # DO dynamics
        dDdt = (do_control - do) / self.config.get('dynamics', {}).get('do', 0.02)
        
        return [dXdt, dTdt, dPhdt, dDdt]
    
    def simulate(self, initial_conditions, control_signals, t_span):
        """
        Run simulation using ODE solver
        """
        # Unpack initial conditions
        y0 = [
            initial_conditions['biomass'],
            initial_conditions['temperature'],
            initial_conditions['ph'],
            initial_conditions['do']
        ]
        
        # Create time vector
        t = np.linspace(0, t_span, int(t_span / self.config.get('simulation', {}).get('time_step', 0.1)))
        
        # Simulate using ODE solver
        y = odeint(self.mass_balance, y0, t, args=(control_signals,))
        
        return {
            'time': t,
            'biomass': y[:, 0],
            'temperature': y[:, 1],
            'ph': y[:, 2],
            'do': y[:, 3]
        }
