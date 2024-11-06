from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy import Energy_Saving

class Energy_Saving_5g(Energy_Saving):
    def __init__(self, main_cell_load, neighbor_cell_loads, saturated_threshold,  carrier_off_threshold, channel_off_threshold, sleep_threshold):
        super().__init__(main_cell_load, neighbor_cell_loads, saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold)

    def perform_sleep(self, hour):
        if self.main_cell_load[hour] < self.sleep_threshold:
            self.schedule[hour] = 'channel_off'
        if hour in self.sleep_hours:
            self.schedule[hour] = 'sleep'

    def is_below_sleep_threshold(self, hour):
        return self.main_cell_load[hour] < self.sleep_threshold

    def get_energy_saving_schedule(self, is_co_covered, channel_T):
        super().get_energy_saving_schedule(is_co_covered, channel_T)
        return self.schedule
