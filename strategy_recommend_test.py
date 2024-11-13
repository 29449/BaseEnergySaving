from base_energy_saving.configuration_data.strategy_data import ConfigurationData
from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy_4g import Energy_Saving_4g
from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.recommend_strategy_5g import Energy_Saving_5g
from base_energy_saving.energy_saving_strategy_recommend.strategy_manager.continuous_time import ContinuousEnergySavingTime
from base_energy_saving.energy_saving_strategy_recommend.threshold_manager.get_threshold import Threshold
import pandas as pd
from glob import glob
import os

def main(file_path):
    # 示例数据
    file_path_main_cell = file_path
    file_path_neighbor_cell_1 = '../testdata/5g_data_with_energy_saving_4915317-258.csv'
    file_path_neighbor_cell_2 = '../testdata/5g_data_with_energy_saving_4933716-259.csv'

    #获取主小区的KPI数据
    df = pd.read_csv(file_path_main_cell)
    df1 = pd.read_csv(file_path_neighbor_cell_1)
    df2 = pd.read_csv(file_path_neighbor_cell_2)
    main_cell_load = df['score']
    is_4g_saving = 0
    neighbor_cell_loads = [df1['score'], df2['score']]

    #调用阈值管理模块
    threshold = Threshold()
    # 调用共覆盖分析模块
    is_co_covered = True
    # 获取T通道数
    data = ConfigurationData(channel_t=2)
    channel_T = data.get_channel_t()

    schedule = []

    batch_size = 96
    # 计算总循环次数
    total_batches = len(main_cell_load) // batch_size + (1 if len(main_cell_load) % batch_size != 0 else 0)
    # 循环处理每96行数据
    for batch_index in range(total_batches):
        # 计算当前批次数据的起始和结束索引
        start_index = batch_index * batch_size
        end_index = start_index + batch_size if batch_index != total_batches - 1 else len(main_cell_load)

        main_cell = main_cell_load[start_index: end_index]
        neighbor_cell = neighbor_cell_loads[start_index: end_index]

        # 获取当前批次的数据
        channel_off_threshold, carrier_off_threshold, sleep_threshold = threshold.calculate_thresholds(threshold.find_max_hour_window(main_cell))
        saturated_threshold = 50

        if is_4g_saving:
            scheduler = Energy_Saving_4g(main_cell, neighbor_cell, saturated_threshold,
                                         carrier_off_threshold,
                                         channel_off_threshold, sleep_threshold)
        else:
            scheduler = Energy_Saving_5g(main_cell, neighbor_cell, saturated_threshold,
                                         carrier_off_threshold,
                                         channel_off_threshold, sleep_threshold)

        schedule_initial = scheduler(is_co_covered, channel_T)
        schedule.append(schedule_initial)

    merged_schedule = [item for sublist in schedule for item in sublist]
    strategy = ContinuousEnergySavingTime()
    schedule_final = {}

    for hour, action in enumerate(merged_schedule):
        schedule_final.update({df['sdate'][hour]: action})

    #for hour, action in schedule_final.items():
        #print(f"{hour}: {action}")

    df['strategy'] = list(schedule_final.values())

    # 11. 保存处理后的数据到新的CSV文件
    file_id = os.path.basename(file_path).split('_')[5].split('.')[0]
    output_path = f'../testdata/5g_data_with_energy_saving_{file_id}.csv'
    df.to_csv(output_path, index=False)
    print(f"处理并填补后的数据已保存至 {output_path}")

    #print("节能调度方案:")
    #strategy.analyze_schedule(schedule_final)

if __name__ == "__main__":
    folder_path = '../testdata/'
    # folder_path_absolute = os.path.abspath(folder_path)  # 转换为绝对路径
    file_paths = glob(os.path.join(folder_path, '*.csv'))

    for file_path in file_paths:
        main(file_path)
