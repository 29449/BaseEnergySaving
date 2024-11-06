class Energy_Saving:
    def __init__(self, main_cell_load, neighbor_cell_loads, saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold):
        """
        初始化节能调度器
        :param main_cell_load: 主小区的负荷数据，一个长度为24的列表，表示每个小时的负荷
        :param neighbor_cell_loads: 邻小区的负荷数据，一个长度为24的二维列表，每个子列表表示一个邻小区每小时的负荷
        :param saturated_threshold: 小区负荷饱和阈值
        :param carrier_off_threshold: 载波类关断阈值
        :param channel_off_threshold: 通道类关断阈值
        :param sleep_threshold: 休眠类阈值
        """
        self.main_cell_load = main_cell_load
        self.neighbor_cell_loads = neighbor_cell_loads
        self.saturated_threshold = saturated_threshold
        self.carrier_off_threshold = carrier_off_threshold
        self.channel_off_threshold = channel_off_threshold
        self.sleep_threshold = sleep_threshold
        self.schedule = ['none'] * 96
        self.sleep_hours = list(range(26))


    def perform_channel_off(self, channel_T, hour):
        #进行通道关断
        if channel_T >= 2:
            self.schedule[hour] = 'channel_off'

    def perform_carrier_off(self, hour):
        #进行载波关断
        pass

    def perform_sleep(self, hour):
        #进行休眠
        pass

    def is_below_carrier_threshold(self, hour):
        #判断是否低于载波关断阈值
        return True

    def is_below_sleep_threshold(self, hour):
        #判断是否低于通道关断阈值
        return True

    def is_neighbor_cells_saturated(self, hour):
        """
        判断所有邻小区在指定小时是否饱和
        :param hour: 时间戳
        :return: 若所有邻小区均饱和则返回True，否则返回False
        """
        for neighbor_load in self.neighbor_cell_loads:
            if neighbor_load[hour] < self.saturated_threshold:
                return False
        return True

    def get_energy_saving_schedule(self, is_co_covered, channel_T):
        for hour in range(96):
            if self.main_cell_load[hour] < self.channel_off_threshold:
                if self.is_below_carrier_threshold(hour):
                    # 如果低于载波关断阈值
                    if self.is_below_sleep_threshold(hour):
                        #如果低于休眠阈值
                        if is_co_covered:
                            # 如果是共覆盖小区
                            if self.is_neighbor_cells_saturated(hour):
                                # 所有邻小区的负荷均饱和
                                self.perform_channel_off(channel_T, hour)
                            else:
                                # 如果有邻小区的负荷未饱和，进行载波关断或者进行休眠
                                self.perform_carrier_off(hour)
                                self.perform_sleep(hour)
                        else:
                            # 如果不是共覆盖小区，则进行通道关断
                            self.perform_channel_off(channel_T, hour)
                    else:
                        #如果高于休眠阈值，则进行通道关断
                        self.perform_channel_off(channel_T, hour)
                else:
                    # 如果高于载波关断阈值，则进行通道关断
                    self.perform_channel_off(channel_T, hour)

