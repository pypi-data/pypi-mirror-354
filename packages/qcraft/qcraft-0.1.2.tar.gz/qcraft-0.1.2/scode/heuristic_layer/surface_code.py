from typing import Dict, Any
from configuration_management.config_manager import ConfigManager
from hardware_abstraction.device_abstraction import DeviceAbstraction
from scode.heuristic_layer.heuristic_initialization_layer import HeuristicInitializationLayer
from scode.multi_patch_mapper.multi_patch_mapper import MultiPatchMapper
from scode.utils.decoder_interface import DecoderInterface
import math

def deep_merge(base: dict, override: dict) -> dict:
    if not override:
        return base.copy()
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

class SurfaceCode:
    def __init__(self, config_overrides: dict = None, device_overrides: dict = None):
        ConfigManager.load_registry()
        base_config = ConfigManager.get_config('multi_patch_rl_agent')
        self.config = deep_merge(base_config, config_overrides or {})
        hardware_json_path = ConfigManager.config_registry['hardware']
        base_device = DeviceAbstraction.load_selected_device(hardware_json_path)
        self.device_config = deep_merge(base_device, device_overrides or {})
        self.h_layer = HeuristicInitializationLayer(self.config, self.device_config)
        self.mapper = MultiPatchMapper(self.config, self.device_config)
        self.current_codes = None
        self.current_mapping = None

    def get_codes(self, code_distance: int, layout_type: str, num_patches: int = 1):
        """
        Generate one or more surface code layouts.
        Args:
            code_distance: Distance of the surface code
            layout_type: Type of surface code layout
            num_patches: Number of code patches to generate (default: 1)
        Returns:
            List of SurfaceCodeObject instances
        """
        config = self.device_config if hasattr(self, 'device_config') else {}
        surface_code_cfg = config.get('multi_patch_rl_agent', {}).get('environment', {})
        min_d = surface_code_cfg.get('min_code_distance', 3)
        if code_distance is None:
            if layout_type in ('planar', 'rotated'):
                max_d = int(math.sqrt(((n/num_patches)+1)/2))
            elif layout_type == 'color':
                max_d = int(math.sqrt(((2*n/num_patches)-1)/3))
            else:
                max_d = int(math.sqrt(n/num_patches))
            best_ler = float('inf')
            best_d = None
            best_mapping = None
            for d in range(min_d, max_d+1, 2):
                try:
                    codes = self.get_codes(d, layout_type, num_patches)
                    if any(not hasattr(code, 'qubit_layout') or not code.qubit_layout for code in codes):
                        raise ValueError(f"Generated patch for code distance {d} is empty or invalid.")
                    mapping = self.mapper.map_patches(codes, mapping_constraints)
                    ler = None
                    try:
                        layout = codes[0] if len(codes) == 1 else codes
                        noise_model = config.get('noise_model', {'p': 0.001})
                        ler = DecoderInterface.estimate_logical_error_rate(layout, mapping, noise_model)
                    except Exception as e:
                        ler = None
                    if ler is not None and ler < best_ler:
                        best_ler = ler
                        best_d = d
                        best_mapping = mapping
                except Exception as e:
                    continue
            # Return best found
            if best_d is not None:
                return self.get_codes(best_d, layout_type, num_patches)
            else:
                raise ValueError("No valid code distance found for given device and layout.")
        # All patch shapes, code distances, and constraints are config-driven
        patch_shapes = surface_code_cfg.get('patch_shapes', ['rectangular'] * num_patches)
        if len(patch_shapes) < num_patches:
            patch_shapes = patch_shapes + [patch_shapes[-1]] * (num_patches - len(patch_shapes))
        self.current_codes = [self.h_layer.generate_surface_code(code_distance, layout_type) for _ in range(num_patches)]
        # Debug: print size and content of each patch's qubit_layout
        for idx, code in enumerate(self.current_codes):
            if not hasattr(code, 'qubit_layout'):
                print(f"[DEBUG] Patch {idx} for d={code_distance} has no qubit_layout attribute!")
            elif not code.qubit_layout:
                print(f"[DEBUG] Patch {idx} for d={code_distance} has EMPTY qubit_layout!")
            else:
                print(f"[DEBUG] Patch {idx} for d={code_distance} qubit_layout size: {len(code.qubit_layout)}")
        # Robustness: check for empty or invalid layouts
        for idx, code in enumerate(self.current_codes):
            if not hasattr(code, 'qubit_layout') or not code.qubit_layout:
                raise ValueError(f"Generated patch {idx} for code distance {code_distance} is empty or invalid.")
        return self.current_codes

    def get_multi_patch_mapping(self, code_distance: int, layout_type: str, mapping_constraints: Dict[str, Any]):
        """
        Returns a mapping dict that always includes 'logical_to_physical' for GUI overlays.
        This is the unified entry point for all mapping requests (single or multi-patch).
        Args:
            code_distance: Distance of the surface code (if None, will be auto-selected)
            layout_type: Type of surface code layout
            mapping_constraints: Dict of mapping constraints (must include 'num_patches' for multi-patch)
        Returns:
            Mapping dictionary
        """
        # l is the number of logical qubits in the circuit
        l = mapping_constraints.get('num_logical_qubits', 1)
        # Only add +1 if code switching is required
        if mapping_constraints.get('require_code_switching', False):
            num_patches = l + 1
        else:
            num_patches = l
        n = self.device_config.get('max_qubits')
        if n is None:
            qc = self.device_config.get('qubit_connectivity')
            if qc:
                n = len(qc)
        if n is None:
            raise ValueError("Device qubit count could not be determined from config.")
        import math
        # --- If code_distance is None, auto-select the best d based on LER ---
        if code_distance is None:
            min_d = 3
            if layout_type in ('planar', 'rotated'):
                max_d = int(math.sqrt(((n/num_patches)+1)/2))
            elif layout_type == 'color':
                max_d = int(math.sqrt(((2*n/num_patches)-1)/3))
            else:
                max_d = int(math.sqrt(n/num_patches))
            best_ler = float('inf')
            best_d = None
            best_mapping = None
            for d in range(min_d, max_d+1, 2):  # Only odd distances
                try:
                    print(f"[DEBUG] Trying code distance {d} for {num_patches} patches...")
                    codes = self.get_codes(d, layout_type, num_patches)
                    if any(not hasattr(code, 'qubit_layout') or not code.qubit_layout for code in codes):
                        print(f"[DEBUG] At least one patch for d={d} is empty or invalid!")
                        raise ValueError(f"Generated patch for code distance {d} is empty or invalid.")
                    mapping = self.mapper.map_patches(codes, mapping_constraints)
                    # Estimate logical error rate (LER) for this mapping using DecoderInterface
                    ler = None
                    try:
                        layout = codes[0] if len(codes) == 1 else codes
                        noise_model = self.device_config.get('noise_model', {'p': 0.001})
                        ler = DecoderInterface.estimate_logical_error_rate(layout, mapping, noise_model)
                    except Exception as e:
                        print(f"[LER ERROR] {e}")
                        ler = None
                    if ler is not None and ler < best_ler:
                        best_ler = ler
                        best_d = d
                        best_mapping = mapping
                except Exception as e:
                    print(f"[WARN] Skipping code distance {d}: {e}")
                    continue  # Skip invalid d
            if best_mapping is None:
                print(f"[DEBUG] No valid code distance found for {num_patches} patches on this device after trying all distances.")
                raise ValueError(f"No valid code distance found for {num_patches} patches on this device.")
            print(f"[INFO] Selected code type: {layout_type}, code distance: {best_d}, LER: {best_ler:.3e}")
            best_mapping['selected_code_distance'] = best_d
            best_mapping['selected_code_type'] = layout_type
            best_mapping['selected_ler'] = best_ler
            self.current_mapping = best_mapping
            return best_mapping
        # --- If code_distance is provided, use as before ---
        code_distance = int(code_distance)
        if layout_type in ('planar', 'rotated'):
            max_d = int(math.sqrt(((n/num_patches)+1)/2))
            required_qubits = num_patches*(2*code_distance*code_distance-1)
            if required_qubits > n:
                print(f"[DEBUG] Not enough physical qubits for {num_patches} planar/rotated patches of distance {code_distance}. Required: {required_qubits}, available: {n}")
                raise ValueError(f"Not enough physical qubits for {num_patches} planar/rotated patches of distance {code_distance}. Max allowed distance: {max_d}, available qubits: {n}")
        elif layout_type == 'color':
            max_d = int(math.sqrt(((2*n/num_patches)-1)/3))
            required_qubits = num_patches*((3*code_distance*code_distance+1)//2)
            if required_qubits > n:
                print(f"[DEBUG] Not enough physical qubits for {num_patches} color code patches of distance {code_distance}. Required: {required_qubits}, available: {n}")
                raise ValueError(f"Not enough physical qubits for {num_patches} color code patches of distance {code_distance}. Max allowed distance: {max_d}, available qubits: {n}")
        else:
            max_d = int(math.sqrt(n/num_patches))
            required_qubits = num_patches*code_distance*code_distance
            if required_qubits > n:
                print(f"[DEBUG] Not enough physical qubits for {num_patches} patches of distance {code_distance}. Required: {required_qubits}, available: {n}")
                raise ValueError(f"Not enough physical qubits for {num_patches} patches of distance {code_distance}. Max allowed distance: {max_d}, available qubits: {n}")
        if code_distance > max_d:
            print(f"[DEBUG] Code distance {code_distance} too large for {num_patches} patches on this device. Max allowed: {max_d}")
            raise ValueError(f"Code distance {code_distance} too large for {num_patches} patches on this device. Max allowed: {max_d}")
        codes = self.get_codes(code_distance, layout_type, num_patches)
        if any(not hasattr(code, 'qubit_layout') or not code.qubit_layout for code in codes):
            print(f"[DEBUG] At least one patch for d={code_distance} is empty or invalid!")
            raise ValueError(f"Generated patch for code distance {code_distance} is empty or invalid.")
        mapping = self.mapper.map_patches(codes, mapping_constraints)
        self.current_mapping = mapping
        print(f"[DEBUG] get_multi_patch_mapping: mapping_constraints={mapping_constraints}")
        print(f"[DEBUG] get_multi_patch_mapping: num_patches={num_patches}")
        patch_shapes = mapping_constraints.get('patch_shapes', None)
        if not patch_shapes or len(patch_shapes) < num_patches:
            default_shape = 'rectangular'
            patch_shapes = (patch_shapes or []) + [default_shape] * (num_patches - len(patch_shapes or []))
        if len(patch_shapes) != num_patches:
            print(f"[WARNING] get_multi_patch_mapping: patch_shapes length {len(patch_shapes)} does not match num_patches {num_patches}")
            print(f"[WARNING] patch_shapes: {patch_shapes}")
            patch_shapes = patch_shapes[:num_patches]
        mapping_constraints['patch_shapes'] = patch_shapes
        print(f"[DEBUG] get_multi_patch_mapping: final patch_shapes={patch_shapes}")
        return mapping 