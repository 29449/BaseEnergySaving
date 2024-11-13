from glob import glob
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# 定义处理单个文件的函数
def process_file(file_path):
    # 加载CSV文件
    df = pd.read_csv(file_path)

    # 确保日期列（例如'sdate'）被正确解析为datetime类型
    df['sdate'] = pd.to_datetime(df['sdate'])

    # 保留第一次出现的时间记录(删除重复)
    df = df.drop_duplicates(subset=['sdate'])

    # 1. 生成完整的时间序列（15分钟为间隔）
    full_time_range = pd.date_range(start=df['sdate'].min(),
                                    end=df['sdate'].max(),
                                    freq='15min')

    # 2. 创建包含完整时间序列的DataFrame，并将其与原始数据合并
    full_data = pd.DataFrame({'sdate': full_time_range})
    df_full = pd.merge(full_data, df, on='sdate', how='left')

    # 3. 对数值型列进行线性插值，填补缺失值
    df_full[['rrc_connmax', 'rrc_connmean', 'prb_useddl', 'prb_availdl']] = df_full[['rrc_connmax', 'rrc_connmean', 'prb_useddl', 'prb_availdl']].interpolate(method='linear')

    # 4. 将 rrc_connmax 列的插值结果四舍五入为整数
    df_full['rrc_connmax'] = df_full['rrc_connmax'].round(0).astype('int')

    # 5. 生成 prb_utilization_rate 列，并处理除零问题
    df_full['prb_dl_utilization_rate'] = df_full.apply(
        lambda row: row['prb_useddl'] / row['prb_availdl'] if row['prb_availdl'] != 0 else 0, axis=1
    )


    # 7. 选取需要归一化的列，包括新的 prb_utilization_rate 列和 prb_availul
    columns_to_normalize = ['prb_dl_utilization_rate', 'rrc_connmax', 'rrc_connmean']

    # 8. 使用 Min-Max 归一化
    scaler = MinMaxScaler()
    df_full[columns_to_normalize] = scaler.fit_transform(df_full[columns_to_normalize])

    # 9. 定义加权评分法
    def energy_saving_strategy_weighted(row):
        # 分配权重
        score = (0.4 * row['prb_dl_utilization_rate'] +
                 0.4 * row['rrc_connmax'] +
                 0.2 * row['rrc_connmean'])

        return score


    # 10. 应用加权节能策略
    df_full['score'] = df_full.apply(energy_saving_strategy_weighted, axis=1)

    # 11. 保存处理后的数据到新的CSV文件
    file_id = os.path.basename(file_path).split('_')[2].split('.')[0]
    output_path = f'../testdata/5g_data_with_energy_saving_{file_id}.csv'
    #output_path = file_path
    df_full.to_csv(output_path, index=False)

    print(f"处理并填补后的数据已保存至 {output_path}")

if __name__ == '__main__':
    #处理单一文件
    #file_path = 'C:/Users/29449/PycharmProjects/baseEnergySaving/base_energy_saving/testdata/5g_data_city_gongshu.csv'
    # 批量处理文件夹中的所有CSV文件
    folder_path = '../testdata/'
    folder_path_absolute = os.path.abspath(folder_path)  # 转换为绝对路径
    file_paths = glob(os.path.join(folder_path, '*.csv'))

    for file_path in file_paths:
        process_file(file_path)
