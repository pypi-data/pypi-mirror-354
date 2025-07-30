from typing import Dict, Any, List, Tuple, Optional, Union
import networkx as nx
import numpy as np

class RewardEngine:
    """
    Reward engine for the surface code RL environment.
    Calculates rewards based on mapping quality, connectivity preservation, and error rates.
    """
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the reward engine with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Load reward weights from config
        self.curriculum_config = config.get('curriculum', {})
        self.phases = self.curriculum_config.get('phases', [{}])
        
        # Default weights (if not in config)
        self.default_weights = {
            'alpha1': 1.0,  # Connectivity preservation weight
            'alpha2': 0.5,  # Error rate optimization weight
            'beta': 0.2,    # Hardware compatibility weight
            'gamma': 0.3,   # Swap/rewire action penalty weight
            'delta': 0.1    # Logical operator integrity weight
        }
        
        # Set up the reward normalization scheme
        self.reward_config = config.get('reward_engine', {})
        self.normalization = self.reward_config.get('normalization', 'none')
        
        # Set up reward normalization tracking
        self.reward_history = []
        self.running_mean = 0.0
        self.running_std = 1.0
        
        # Phase-specific multipliers
        self.phase_multipliers = self.reward_config.get('phase_multipliers', {})
        
        # Verbosity flag
        self.verbose = config.get('system', {}).get('log_level', 'INFO') == 'DEBUG'

    def calculate_reward(self, surface_code, mapping: Dict[int, int], 
                        hw_graph: nx.Graph, action_type: int, 
                        current_phase: int) -> float:
        """
        Calculate the reward for the current state and action.
        
        Args:
            surface_code: SurfaceCodeObject containing the surface code layout
            mapping: Dictionary mapping surface code qubits to hardware qubits
            hw_graph: NetworkX graph representing hardware connectivity
            action_type: Type of action taken (0=SWAP, 1=REWIRE, 2=ASSIGN_GATE)
            current_phase: Current curriculum learning phase
            
        Returns:
            Calculated reward value
        """
        # Get the weights for the current phase
        weights = self._get_phase_weights(current_phase)
        
        # Calculate component rewards
        conn_reward = weights['alpha1'] * self._connectivity_reward(surface_code, mapping, hw_graph)
        error_reward = weights['alpha2'] * self._error_rate_reward(surface_code, mapping, hw_graph)
        
        # Penalty for expensive actions
        action_penalty = 0.0
        if action_type == 0:  # SWAP
            action_penalty = weights['gamma'] * 0.1  # Small penalty for SWAPs
        elif action_type == 1:  # REWIRE
            action_penalty = weights['gamma'] * 0.2  # Larger penalty for rewiring
            
        # Calculate logical operator integrity reward
        logical_reward = weights['delta'] * self._logical_operator_reward(surface_code, mapping, hw_graph)
        
        # Combine all rewards
        total_reward = conn_reward + error_reward - action_penalty + logical_reward
        
        # Normalize reward if configured
        normalized_reward = self._normalize_reward(total_reward)
        
        return normalized_reward

    def _get_phase_weights(self, current_phase: int) -> Dict[str, float]:
        """
        Get the reward weights for the current curriculum phase.
        
        Args:
            current_phase: Current curriculum learning phase
            
        Returns:
            Dictionary of reward weights
        """
        # Default to base weights
        weights = self.default_weights.copy()
        
        # Override with phase-specific weights if available
        if current_phase < len(self.phases):
            phase_weights = self.phases[current_phase].get('reward_weights', {})
            weights.update({k: v for k, v in phase_weights.items() if v is not None})
        
        # Apply phase-specific multipliers if dynamic weights are enabled
        if self.dynamic_weights:
            # Structure mastery phase (focuses on stabilizer integrity)
            if current_phase == 0:
                multiplier = self.phase_multipliers.get('structure_mastery_stabilizer', 1.0)
                weights['epsilon'] *= multiplier
                
            # Hardware adaptation phase (focuses on connectivity and SWAPs)
            elif current_phase == 1:
                conn_multiplier = self.phase_multipliers.get('hardware_adaptation_gate_error', 1.0)
                swap_multiplier = self.phase_multipliers.get('hardware_adaptation_swap', 1.0)
                weights['alpha1'] *= conn_multiplier
                weights['gamma'] *= swap_multiplier
                
            # Noise-aware optimization phase (focuses on error rates)
            elif current_phase == 2:
                error_multiplier = self.phase_multipliers.get('noise_aware_logical_error', 1.0)
                weights['alpha2'] *= error_multiplier
                weights['delta'] *= error_multiplier
        
        return weights

    def _connectivity_reward(self, surface_code, mapping: Dict[int, int], 
                           hw_graph: nx.Graph) -> float:
        """
        Calculate reward based on connectivity preservation.
        
        Args:
            surface_code: SurfaceCodeObject containing the surface code layout
            mapping: Dictionary mapping surface code qubits to hardware qubits
            hw_graph: NetworkX graph representing hardware connectivity
            
        Returns:
            Connectivity preservation reward
        """
        # Count preserved edges
        preserved_edges = 0
        total_edges = 0
        
        for sc_q1, sc_q2 in surface_code.adjacency_matrix.edges():
            total_edges += 1
            
            if sc_q1 in mapping and sc_q2 in mapping:
                hw_q1 = mapping[sc_q1]
                hw_q2 = mapping[sc_q2]
                
                if hw_graph.has_edge(hw_q1, hw_q2):
                    preserved_edges += 1
        
        # Calculate the ratio of preserved edges
        if total_edges == 0:
            connectivity_score = 1.0  # Perfect score if no edges
        else:
            connectivity_score = preserved_edges / total_edges
        
        return connectivity_score

    def _error_rate_reward(self, surface_code, mapping: Dict[int, int], 
                         hw_graph: nx.Graph) -> float:
        """
        Calculate reward based on error rate optimization.
        
        Args:
            surface_code: SurfaceCodeObject containing the surface code layout
            mapping: Dictionary mapping surface code qubits to hardware qubits
            hw_graph: NetworkX graph representing hardware connectivity
            
        Returns:
            Error rate optimization reward
        """
        # Calculate average error rate of mapped qubits
        total_error = 0.0
        qubit_count = 0
        
        for sc_q, hw_q in mapping.items():
            if hw_q in hw_graph.nodes:
                error_rate = hw_graph.nodes[hw_q].get('error_rate', 0.0)
                total_error += error_rate
                qubit_count += 1
        
        # Calculate the error score (lower is better, so invert)
        if qubit_count == 0:
            avg_error = 1.0
        else:
            avg_error = total_error / qubit_count
        
        # Invert to get a reward (higher is better)
        error_score = 1.0 - avg_error
        
        return error_score

    def _logical_operator_reward(self, surface_code, mapping: Dict[int, int], 
                              hw_graph: nx.Graph) -> float:
        """
        Calculate reward based on logical operator integrity.
        
        Args:
            surface_code: SurfaceCodeObject containing the surface code layout
            mapping: Dictionary mapping surface code qubits to hardware qubits
            hw_graph: NetworkX graph representing hardware connectivity
            
        Returns:
            Logical operator integrity reward
        """
        # Check if logical operators are properly connected in hardware
        logical_x = surface_code.logical_operators.get('X', [])
        logical_z = surface_code.logical_operators.get('Z', [])
        
        # Count correctly mapped logical qubits
        x_mapped = sum(1 for q in logical_x if q in mapping)
        z_mapped = sum(1 for q in logical_z if q in mapping)
        
        # Calculate the logical operator mapping ratio
        if not logical_x and not logical_z:
            return 0.0  # No logical operators defined
            
        x_ratio = x_mapped / max(1, len(logical_x))
        z_ratio = z_mapped / max(1, len(logical_z))
        
        # Average the ratios
        logical_score = (x_ratio + z_ratio) / 2.0
        
        return logical_score

    def _normalize_reward(self, reward: float) -> float:
        """
        Normalize the reward based on the configured normalization scheme.
        
        Args:
            reward: Raw reward value
            
        Returns:
            Normalized reward
        """
        # Track reward history
        self.reward_history.append(reward)
        
        # Apply normalization based on configuration
        if self.normalization == 'none':
            return reward
            
        elif self.normalization == 'running_mean_std':
            # Update running statistics
            if len(self.reward_history) == 1:
                self.running_mean = reward
                self.running_std = 1.0
            else:
                # Exponential moving average
                alpha = 0.01  # Low alpha for stability
                self.running_mean = (1 - alpha) * self.running_mean + alpha * reward
                self.running_std = (1 - alpha) * self.running_std + alpha * abs(reward - self.running_mean)
                self.running_std = max(0.1, self.running_std)  # Prevent division by very small values
            
            # Normalize using running statistics
            normalized = (reward - self.running_mean) / self.running_std
            
            # Clip to a reasonable range
            return max(-5.0, min(5.0, normalized))
            
        elif self.normalization == 'clip':
            # Simple clipping to a range
            return max(-1.0, min(1.0, reward))
            
        elif self.normalization == 'percentile':
            # If we have enough history, use percentile-based normalization
            if len(self.reward_history) > 100:
                sorted_rewards = sorted(self.reward_history[-100:])
                percentile_5 = sorted_rewards[4]  # 5th percentile
                percentile_95 = sorted_rewards[94]  # 95th percentile
                
                if percentile_95 > percentile_5:
                    normalized = (reward - percentile_5) / (percentile_95 - percentile_5)
                    return max(0.0, min(1.0, normalized))
            
            # Not enough history or identical values
            return max(0.0, min(1.0, reward))
        
        # Default fallback
        return reward 