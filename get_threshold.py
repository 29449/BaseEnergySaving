import numpy as np

class Threshold:
    def __init__(self):
        pass

    def find_max_hour_window(self, values, interval=4):
        """找到最大的一段连续一个小时的数据"""
        num_samples = len(values)
        max_sum = float('-inf')
        max_window = []

        for i in range(num_samples - interval + 1):
            window_values = values[i:i + interval]
            window_sum = np.sum(window_values)
            if window_sum > max_sum:
                max_sum = window_sum
                max_window = window_values

        return max_window

    def calculate_thresholds(self, window_values):
        """计算平均值和阈值"""
        average = np.mean(window_values)
        channel_off_threshold = average * 0.4
        carrier_off_threshold = average * 0.3
        sleep_threshold = average * 0.2
        return channel_off_threshold, carrier_off_threshold, sleep_threshold
