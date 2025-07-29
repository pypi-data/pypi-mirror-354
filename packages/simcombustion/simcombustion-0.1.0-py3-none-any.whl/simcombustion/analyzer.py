# Archivo: simcombustion/analyzer.py

import cantera as ct
import numpy as np
import importlib.resources

_DATA_PATH = importlib.resources.files('simcombustion.data')
_MECHANISM_PATH = str(_DATA_PATH.joinpath('91sp_991re.yaml'))


class CombustionAnalyzer:
    """
    Una clase para analizar procesos de combustión utilizando un mecanismo '91sp_991re.yaml' empaquetado.
    """
    mechanism_file = _MECHANISM_PATH

    def __init__(self, fuel_name):
        self.fuel_name = fuel_name
        self.gas_template = ct.Solution(self.mechanism_file)

        if self.fuel_name not in self.gas_template.species_names:
            raise ValueError(f"Combustible '{self.fuel_name}' no encontrado. Use `list_available_fuels()`.")

        print(f"INFO: Inicializando analizador para combustible '{self.fuel_name}'")

        try:
            self.pci = self._calcular_pci()
            if not np.isfinite(self.pci):
                raise ValueError("El cálculo de PCI resultó en un valor no finito.")
            print(f"INFO: PCI para {self.fuel_name}: {self.pci / 1e6:.4f} MJ/kg")
        except Exception as e:
            raise ValueError(f"No se pudo inicializar CombustionAnalyzer: {e}") from e

    @staticmethod
    def list_available_fuels():
        gas = ct.Solution(_MECHANISM_PATH)
        return gas.species_names

    def _calcular_pci(self):
        gas_pci = ct.Solution(self.mechanism_file)
        gas_pci.TP = 298.15, ct.one_atm
        gas_pci.set_equivalence_ratio(1.0, self.fuel_name, 'O2:1.0')
        h_reactants = gas_pci.enthalpy_mass
        try:
            fuel_idx = gas_pci.species_index(self.fuel_name)
            fuel_mass_frac = gas_pci.Y[fuel_idx]
        except ValueError:
            raise ValueError(f"PCI Error: Combustible '{self.fuel_name}' no encontrado.")
        if fuel_mass_frac < 1e-9:
            raise ValueError("PCI Error: La fracción másica del combustible es demasiado baja.")
        gas_pci.equilibrate('TP')
        h_products = gas_pci.enthalpy_mass
        pci = -(h_products - h_reactants) / fuel_mass_frac
        return pci

    def _inicializar_nan_results(self):
        """Devuelve un diccionario con todos los resultados inicializados a NaN."""
        return {
            'T_out_K': np.nan,
            'efficiency_pct': np.nan,
            'X_NOx_total': np.nan,
            'X_fuel_unburned': np.nan,
            'X_CO_out': np.nan,
            'X_CO2_out': np.nan,
            'X_other_HC_out': np.nan
        }

    def calcular_propiedades(self, rel_equivalencia, T_in_K, P_in_atm, tiempo_residencia_s):
        """
        Calcula las propiedades de la combustión para unas condiciones de entrada dadas.
        """
        if not (self.pci > 1e-9):
            print("ERROR: PCI no es válido.")
            return self._inicializar_nan_results()

        gas_inlet = ct.Solution(self.mechanism_file)
        gas_inlet.TP = T_in_K, P_in_atm * ct.one_atm
        try:
            gas_inlet.set_equivalence_ratio(rel_equivalencia, self.fuel_name, 'O2:1.0, N2:3.76')
        except ct.CanteraError:
            return self._inicializar_nan_results()

        h_reactants_at_Tin = gas_inlet.enthalpy_mass
        y_fuel_in = gas_inlet.Y[gas_inlet.species_index(self.fuel_name)]

        inlet_res = ct.Reservoir(gas_inlet)

        gas_reactor_init = ct.Solution(self.mechanism_file)
        gas_reactor_init.TPX = gas_inlet.TPX
        try:
            gas_reactor_init.equilibrate('HP')
        except ct.CanteraError as e:
            gas_reactor_init.TPX = gas_inlet.TPX

        reactor = ct.IdealGasReactor(gas_reactor_init)
        exhaust_res = ct.Reservoir(gas_reactor_init)

        def mdot(t):
            return reactor.mass / tiempo_residencia_s

        inlet_mfc = ct.MassFlowController(inlet_res, reactor, mdot=mdot)
        outlet_valve = ct.PressureController(reactor, exhaust_res, primary=inlet_mfc, K=0.01)

        sim = ct.ReactorNet([reactor])
        sim.advance_to_steady_state()

        final_thermo_state = reactor.thermo

        gas_products_at_Tin = ct.Solution(self.mechanism_file)
        gas_products_at_Tin.TPX = T_in_K, final_thermo_state.P, final_thermo_state.X
        h_products_at_Tin = gas_products_at_Tin.enthalpy_mass

        heat_released = h_reactants_at_Tin - h_products_at_Tin
        max_heat_possible = y_fuel_in * self.pci

        efficiency_pct = np.nan
        if abs(max_heat_possible) > 1e-12:
            efficiency_fraction = heat_released / max_heat_possible
            efficiency_pct = np.clip(efficiency_fraction, 0.0, 1.2)*100

        X_products = final_thermo_state.X
        species_names = final_thermo_state.species_names

        idx_NO = species_names.index('NO') if 'NO' in species_names else -1
        idx_NO2 = species_names.index('NO2') if 'NO2' in species_names else -1

        X_NOx = (X_products[idx_NO] if idx_NO != -1 else 0) + (X_products[idx_NO2] if idx_NO2 != -1 else 0)
        X_fuel = X_products[species_names.index(self.fuel_name)]
        X_CO = X_products[species_names.index('CO')]
        X_CO2 = X_products[species_names.index('CO2')]

        X_otros_HC = 0.0
        for i, name in enumerate(species_names):
            species = final_thermo_state.species(i)
            if 'C' in species.composition and 'H' in species.composition:
                if name not in [self.fuel_name, 'CO', 'CO2']:
                    X_otros_HC += X_products[i]

        return {
            'T_out_K': reactor.T,
            'efficiency_pct': efficiency_pct,
            'X_NOx': X_NOx,
            'X_fuel_inquemado': X_fuel,
            'X_CO': X_CO,
            'X_CO2': X_CO2,
            'X_otros_HC': X_otros_HC
        }