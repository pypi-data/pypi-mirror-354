import dask.array as da
import zarr
import os

class DaskZarrIO:
    """
    用于高效读写Zarr文件的Dask封装类
    """
    
    def __init__(self, input_path=None, output_path=None, expected_shape=None, chunks=None, tile='/0/0/'):
        """
        初始化参数
        :param input_path: 输入Zarr文件路径
        :param output_path: 输出Zarr文件路径
        :param expected_shape: 预期数组形状
        :param chunks: 分块大小
        """
        self.input_path = input_path
        self.output_path = output_path
        self.expected_shape = expected_shape
        self.chunks = chunks
        self.tile = tile
        
    
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"输入文件不存在: {self.input_path}")
            
        if not os.path.exists(self.input_path + tile + 'traces'):
            raise FileNotFoundError(f"traces数据不存在: {self.input_path + tile + 'traces'}")
        self.t = da.from_zarr(self.input_path + tile + 'traces')
        self.num_samples = self.t.shape[1]
        self.sel_num_samples = self.num_samples
        self.num_traces = self.t.shape[0]
        self.sel_num_traces = self.num_traces
        self.trace_range = (0, self.num_traces)
        self.sample_range = (0, self.num_samples)
        if os.path.exists(self.input_path+tile+'plaintext'):
            self.plaintext = da.from_zarr(self.input_path+tile+'plaintext')
        else:
            self.plaintext = None
        if os.path.exists(self.input_path+tile+'key'):
            self.key = da.from_zarr(self.input_path+tile+'key')
        else:
            self.key = None
        if os.path.exists(self.input_path+tile+'ciphertext'):
            self.metadata = da.from_zarr(self.input_path+tile+'ciphertext')
        else:
            self.metadata = None

    def set_range(self, trace_range=None, sample_range=None):
        """
        设置读取范围
        :param trace_range: 读取的trace范围，默认为全范围
        :param sample_range: 读取的sample范围，默认为全范围
        """
        if trace_range is None:
            self.trace_range = (0, self.num_traces)
        else:
            self.trace_range = trace_range
            self.sel_num_traces = trace_range[1] - trace_range[0]
        if sample_range is None:
            self.sample_range = (0, self.num_samples)
        else:
            self.sample_range = sample_range
            self.sel_num_samples = sample_range[1] - sample_range[0]

    
    def read(self):
        """
        读取Zarr文件为Dask数组
        :return: Dask数组
        """
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"输入文件不存在: {self.input_path}")
            
        dask_array = da.from_zarr(self.input_path)
        
        # if self.expected_shape and dask_array.shape != tuple(self.expected_shape):
        #     raise ValueError(f"数组形状不匹配，预期: {self.expected_shape}, 实际: {dask_array.shape}")
            
        print(f"Dask数组形状: {dask_array.shape}")
        print(f"Dask数组块大小: {dask_array.chunks}")
        return dask_array
    
    def write(self, dask_array):
        """
        将Dask数组写入Zarr文件
        :param dask_array: 要写入的Dask数组
        """
        if not self.output_path:
            raise ValueError("未指定输出路径")
            
        if self.chunks:
            dask_array = dask_array.rechunk(self.chunks)
            
        dask_array.to_zarr(self.output_path, overwrite=True)
        print(f"数据已写入: {self.output_path}")
        
        

# 保留原有函数作为兼容接口
def read_zarr_with_dask(zarr_path):
    """兼容旧版读取函数"""
    return DaskZarrIO(input_path=zarr_path).read()

def write_dask_to_zarr(dask_array, output_path):
    """兼容旧版写入函数"""
    DaskZarrIO(output_path=output_path).write(dask_array)



def merge_zarr_files(file1, file2, output_file, tile='/0/0/', axis=0):
    """
    合并两个zarr文件并保存到输出文件
    :param file1: 第一个zarr文件路径
    :param file2: 第二个zarr文件路径
    :param output_file: 输出文件路径
    :param axis: 合并轴，0为垂直合并，1为水平合并
    :return: 合并后的Dask数组
    """

    store = zarr.DirectoryStore(output_file)
    root = zarr.group(store=store, overwrite=True)
    # 加载两个文件的曲线
    arr1 = da.from_zarr(file1+tile+'traces')
    arr2 = da.from_zarr(file2+tile+'traces')  
    # 检查形状是否兼容
    if axis == 0 and arr1.shape[1:] != arr2.shape[1:]:
        raise ValueError("垂直合并时除第一维外其他维度必须相同")
    if axis == 1 and arr1.shape[0] != arr2.shape[0]:
        raise ValueError("水平合并时第一维必须相同")
    # 合并数组
    merged = da.concatenate([arr1, arr2], axis=axis)
    # 创建traces数据集
    root.create_dataset(
        '/0/0/traces', 
        shape=(merged.shape[0], merged.shape[1]),
        data = merged.compute()
    )
    #TODO: 合并明文、密文和密钥

    # 加载file1的traces数据集
    file1_store = zarr.DirectoryStore(file1)
    file1_root = zarr.group(store=file1_store)

    # 将输出文件的attrs设为和file1一致
    root.attrs.update(file1_root.attrs)
    


if __name__ == "__main__":
    # 示例用法
    input_path = "E:\\codes\\template\\dataset\\20250221202721.zarr"
    output_path = "dataset/dask_output.zarr"
    
    test = DaskZarrIO(input_path=input_path)
    print(test.t[0].compute())
    
    # 读取示例
    # dask_data = read_zarr_with_dask(input_path)
    
    # # 对数据进行一些操作（示例：计算均值）
    # mean_value = dask_data.mean().compute()
    # print(f"数据均值: {mean_value}")
    
    # 写入示例
    # write_dask_to_zarr(dask_data, output_path)