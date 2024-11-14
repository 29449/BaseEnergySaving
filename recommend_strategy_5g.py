from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy import EnergySaving
import numpy as np

class EnergySaving5g(EnergySaving):
    def __init__(self, saturated_threshold,  carrier_off_threshold, channel_off_threshold, sleep_threshold):
        super().__init__(saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold)

    def perform_sleep(self, time, schedule, hours_to_process_sleep, unsaturated_neighbors_mask):
        unsaturated_hours_sleep = np.where(unsaturated_neighbors_mask)[0]
        schedule[unsaturated_hours_sleep] = '1'
        for hour in unsaturated_hours_sleep:
            if (time[hour].hour >= 0) & (time[hour].hour < 6):
                schedule[hour] = '3'

    def is_below_sleep_threshold(self, load):
        return load < self.sleep_threshold

    def __call__(self, time, main_cell_load, neighbor_cell_loads, is_co_covered, channel_T):
        schedule = super().get_energy_saving_schedule(time, main_cell_load, neighbor_cell_loads, is_co_covered, channel_T)
        return schedule
