from base_energy_saving.energy_saving_analysis.strategy_manager.strategy_recommend import EnergySavingStrategyManager
from base_energy_saving.configuration_data.threshold_manager import ThresholdManager
from base_energy_saving.configuration_data.strategy_data import ConfigurationData
from base_energy_saving.energy_saving_analysis.strategy_manager.strategy import EnergySavingManager
import pandas as pd

def main():
    # 示例数据
    file_path_main_cell = 'C:/Users/29449/Desktop/dataset/main_cell.xlsx'
    file_path_neighbor_cell_1 = 'C:/Users/29449/Desktop/dataset/neighbor_cell_1.xlsx'
    file_path_neighbor_cell_2 = 'C:/Users/29449/Desktop/dataset/neighbor_cell_2.xlsx'

    #获取主小区的KPI数据
    df = pd.read_excel(file_path_main_cell)
    df1 = pd.read_excel(file_path_neighbor_cell_1)
    df2 = pd.read_excel(file_path_neighbor_cell_2)
    main_cell_load = df.iloc[:97, df.columns.get_loc('rrc_connmax')]

    # 调用共覆盖分析模块，获取基于该主小区所有邻小区的KPI数据
    neighbor_cell_loads = [df1.iloc[:97, df1.columns.get_loc('rrc_connmax')],
                              df2.iloc[:97, df2.columns.get_loc('rrc_connmax')]]

    # 调用阈值管理模块
    threshold = ThresholdManager(channel_off_threshold = 20, carrier_off_threshold = 10, sleep_threshold = 10, saturated_threshold = 50)
    carrier_off_threshold = threshold.get_carrier_off_threshold()
    channel_off_threshold = threshold.get_channel_off_threshold()
    sleep_threshold = threshold.get_sleep_threshold()
    saturated_threshold = threshold.get_saturated_threshold()

    # 调用共覆盖分析模块
    is_co_covered = True
    is_4g_saving = 0

    # 获取T通道数
    data = ConfigurationData(channel_t = 2)
    channel_T = data.get_channel_t()

    scheduler = EnergySavingStrategyManager(main_cell_load, neighbor_cell_loads, saturated_threshold, carrier_off_threshold, channel_off_threshold, sleep_threshold)
    schedule = scheduler.get_energy_saving_schedule(is_co_covered, channel_T, is_4g_saving)
    strategy = EnergySavingManager(neighbor_cell_loads, saturated_threshold)
    schedule_final = {}

    for hour, action in enumerate(schedule):
        schedule_final.update({df['sdate'][hour]: action})

    for hour, action in schedule_final.items():
        print(f"{hour}: {action}")

    print("节能调度方案:")
    strategy.analyze_schedule(schedule_final)

if __name__ == "__main__":
    main()