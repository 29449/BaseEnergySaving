from base_energy_saving.energy_saving_analysis.strategy_manager.strategy import EnergySavingManager
class EnergySavingStrategyManager:
    def __init__(self, main_cell_load, neighbor_cell_loads, saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold):
        """
        初始化节能调度器
        :param main_cell_load: 主小区的负荷数据，一个长度为24的列表，表示每个小时的负荷
        :param neighbor_cell_loads: 邻小区的负荷数据，一个长度为24的二维列表，每个子列表表示一个邻小区每小时的负荷
        :param saturated_threshold: 小区负荷饱和阈值
        :param carrier_off_threshold: 载波类关断阈值
        :param channel_off_threshold: 通道类关断阈值
        """
        self.main_cell_load = main_cell_load
        self.neighbor_cell_loads = neighbor_cell_loads
        self.saturated_threshold = saturated_threshold
        self.carrier_off_threshold = carrier_off_threshold
        self.channel_off_threshold = channel_off_threshold
        self.sleep_threshold = sleep_threshold
        self.str = EnergySavingManager(neighbor_cell_loads, saturated_threshold)

    def get_energy_saving_schedule(self, is_co_covered, channel_T, is_4g_saving):
        """
        获取节能调度方案
        :return: 一个长度为24的列表，表示每个小时的节能措施
                 'carrier_off' 表示载波类关断
                 'channel_off' 表示通道类关断
                 'none' 表示不进行节能操作
        """
        schedule = ['none'] * 96
        sleep_hours = list(range(26))
        for hour in range(96):
            if self.main_cell_load[hour] < self.channel_off_threshold:
                if self.main_cell_load[hour] < self.carrier_off_threshold:
                    # 如果低于载波关断阈值
                    if is_co_covered:
                        # 如果是共覆盖小区
                        if self.str.is_neighbor_cells_saturated(hour):
                            # 所有邻小区的负荷均饱和
                            if channel_T >= 2:
                                #判断通道数
                                schedule[hour] = 'channel_off'
                        else:
                            # 如果有邻小区的负荷未饱和
                            if is_4g_saving:
                                schedule[hour] = 'carrier_off'
                            else:
                                if self.main_cell_load[hour] < self.sleep_threshold:
                                    schedule[hour] = 'channel_off'
                                if hour in sleep_hours and self.main_cell_load[hour] < self.sleep_threshold:
                                    schedule[hour] = 'sleep'
                    else:
                        # 如果不是共覆盖小区
                        if channel_T >= 2:
                            schedule[hour] = 'channel_off'
                else:
                    # 如果高于载波关断阈值
                    if channel_T >= 2:
                        schedule[hour] = 'channel_off'

        return schedule

