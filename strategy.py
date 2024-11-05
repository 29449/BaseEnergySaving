from datetime import timedelta, datetime
class EnergySavingManager:
    def __init__(self, neighbor_cell_loads, saturated_threshold):
        self.neighbor_cell_loads = neighbor_cell_loads
        self.saturated_threshold = saturated_threshold

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

    def analyze_schedule(self, schedule):
        # 时长连续性判断
        # 将调度方案转换为易于处理的格式
        events = []
        for time, action in schedule.items():
            events.append((time, action))

        # 按时间排序（虽然输入已经排序，但这里确保万无一失）
        events.sort(key=lambda x: x[0])

        # 初始化变量
        current_start = None
        current_action = None
        carrier_or_sleep_count = 0
        mixed_count = 0

        # 遍历事件
        for i, (time, action) in enumerate(events):
            if current_action is None:
                # 开始新的事件段
                current_start = time
                current_action = action
                if action == 'carrier_off' or action == 'sleep':
                    carrier_or_sleep_count = 1
                    mixed_count = 1
                elif action == 'channel_off':
                    carrier_or_sleep_count = 0
                    mixed_count = 1
                else:
                    carrier_or_sleep_count = 0
                    mixed_count = 0
            else:
                if action == 'carrier_off' or action == 'sleep':
                    carrier_or_sleep_count += 1
                    mixed_count += 1
                elif action == 'channel_off':
                    mixed_count += 1
                #如果是无节能时段，立即判断之前节能策略时长连续性，并进行输出
                else:
                    if (current_action == 'carrier_off' or current_action == 'sleep') and carrier_or_sleep_count >= 4:
                        self.print_sleep_period(current_start, events[i][0], current_action)
                        current_start = time
                        current_action = action
                        carrier_or_sleep_count = 0
                        mixed_count = 0
                    elif (current_action == 'channel_off' or (
                            (current_action == 'carrier_off' or current_action == 'sleep') and carrier_or_sleep_count < 4)) and mixed_count >= 8:
                        self.print_mixed_period(current_start, events[i][0])
                        current_start = time
                        current_action = action
                        carrier_or_sleep_count = 0
                        mixed_count = 0
                    else:
                        current_start = time
                        current_action = action
                        carrier_or_sleep_count = 0
                        mixed_count = 0

                # 检查是否继续当前事件段
                if action == current_action:
                    continue
                else:
                    # 事件段结束，检查并输出
                    if (current_action == 'carrier_off' or current_action == 'sleep') and carrier_or_sleep_count >= 4:
                        self.print_sleep_period(current_start, events[i][0], current_action)
                        current_start = time
                        current_action = action
                        if action == 'carrier_off' or action == 'sleep':
                            carrier_or_sleep_count = 1
                            mixed_count = 1
                        elif action == 'channel_off':
                            mixed_count = 1
                            carrier_or_sleep_count = 0
                        else:
                            carrier_or_sleep_count = 0
                            mixed_count = 0

                    elif (current_action == 'channel_off' or (
                            (current_action == 'carrier_off' or current_action == 'sleep') and carrier_or_sleep_count < 4)) and mixed_count >= 8:
                        self.print_mixed_period(current_start, events[i][0])
                        current_start = time
                        current_action = action
                        if action == 'carrier_off' or action == 'sleep':
                            carrier_or_sleep_count = 1
                            mixed_count = 1
                        elif action == 'channel_off':
                            mixed_count = 1
                            carrier_or_sleep_count = 0
                        else:
                            carrier_or_sleep_count = 0
                            mixed_count = 0

                    else:
                        current_action = action

        # 检查最后一个事件段
        if (current_action == 'carrier_off' or current_action == 'sleep') and carrier_or_sleep_count >= 4:
            self.print_sleep_period(current_start, events[0][0], current_action)
        elif (current_action == 'channel_off' or (
                (current_action == 'carrier_off' or current_action == 'sleep') and carrier_or_sleep_count < 4)) and mixed_count >= 8:
            self.print_mixed_period(current_start, events[0][0])

    def print_sleep_period(self, start, end, current_action):
        duration = end - start
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        print(
            f"from {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')} ({hours}h {minutes}m): {current_action}")

    def print_mixed_period(self, start, end):
        duration = end - start
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        print(
            f"from {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')} ({hours}h {minutes}m): channel_off")

