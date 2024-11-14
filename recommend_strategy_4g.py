from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy import EnergySaving
import numpy as np

class EnergySaving4g(EnergySaving):
    def __init__(self, saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold):
        super().__init__(saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold)

    def perform_carrier_off(self, schedule, hours_to_process_carrier, unsaturated_neighbors_mask):
        unsaturated_hours_carrier = np.where(unsaturated_neighbors_mask)[0]
        schedule[unsaturated_hours_carrier] = '2'

    def is_below_carrier_threshold(self, load):
        return load < self.carrier_off_threshold

    def __call__(self, time, main_cell_load, neighbor_cell_loads, is_co_covered, channel_T):
        schedule = super().get_energy_saving_schedule(time, main_cell_load, neighbor_cell_loads, is_co_covered, channel_T)
        return schedule
