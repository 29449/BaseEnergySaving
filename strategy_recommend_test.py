from base_energy_saving.configuration_data.strategy_data import ConfigurationData
from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy_4g import EnergySaving4g
from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy_5g import EnergySaving5g
from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.continuous_time import ContinuousEnergySavingTime
from base_energy_saving.energy_saving_strategy_recommend.threshold_manager.get_threshold import Threshold
import pandas as pd
import os

def main(file_path):
    # 示例数据
    file_path_main_cell = file_path
    file_path_neighbor_cell_1 = '../testdata/5g_data_with_energy_saving_4915211-1537.csv'
    file_path_neighbor_cell_2 = '../testdata/5g_data_with_energy_saving_4915211-1538.csv'
    file_path_threshold = 'C:/Users/29449/PycharmProjects/baseEnergySaving/base_energy_saving/testdata/5g_data_city_gongshu.csv'

    # 读取主小区及其邻小区的的KPI数据的文件，另外还读取某乡镇一天的平均KPI数据文件
    df = pd.read_csv(file_path_main_cell)
    df1 = pd.read_csv(file_path_neighbor_cell_1)
    df2 = pd.read_csv(file_path_neighbor_cell_2)
    df3 = pd.read_csv(file_path_threshold)

    # 当前主小区为5G小区
    is_4g_saving = 0

    # 获取待处理的时间，获取主小区及其邻小区的KPI数据，另外还获取某乡镇一天的平均KPI数据
    time = pd.to_datetime(df['sdate'])
    main_cell_load = df['score'].to_numpy()
    neighbor_cell_loads = [df1['score'].to_numpy(), df2['score'].to_numpy()]
    load_threshold = df3['score']

    # 调用阈值管理模块
    threshold = Threshold()
    channel_off_threshold, carrier_off_threshold, sleep_threshold = threshold.calculate_thresholds(threshold.find_max_hour_window(load_threshold))
    saturated_threshold = 50

    # 调用共覆盖分析模块
    is_co_covered = True

    # 获取T通道数
    data = ConfigurationData(channel_t=2)
    channel_T = data.get_channel_t()

    # 通过判断小区是4/5G，分别调用对应的策略推荐模块
    if is_4g_saving:
        scheduler = EnergySaving4g(saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold)
    else:
        scheduler = EnergySaving5g(saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold)

    schedule = scheduler(time, main_cell_load, neighbor_cell_loads, is_co_covered, channel_T)
    # strategy = ContinuousEnergySavingTime()
    schedule_final = {}

    for hour, action in enumerate(schedule):
        schedule_final.update({df['sdate'][hour]: action})

    df['strategy'] = list(schedule_final.values())

    # 保存处理后的数据到新的CSV文件
    file_id = os.path.basename(file_path).split('_')[5].split('.')[0]
    output_path = f'../testdata/5g_data_with_energy_saving_{file_id}.csv'
    df.to_csv(output_path, index=False)
    print(f"处理并填补后的数据已保存至 {output_path}")

if __name__ == "__main__":
    # 定义文件名的模式
    file_names = ['../testdata/5g_data_with_energy_saving_4915211-1537.csv',
                  '../testdata/5g_data_with_energy_saving_4915211-1538.csv',
                  '../testdata/5g_data_with_energy_saving_4915211-1539.csv',
                  '../testdata/5g_data_with_energy_saving_4915316-1538.csv',
                  '../testdata/5g_data_with_energy_saving_4915321-258.csv']

    for file_path in file_names:
        main(file_path)
