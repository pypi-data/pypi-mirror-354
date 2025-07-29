from traceIO import DaskZarrIO
import dask.array as da
import os

class PPBasic(DaskZarrIO):
    def __init__(self, input_path=None, output_path=None, tile='/0/0/', **kwargs):
        super().__init__(input_path=input_path, output_path=output_path, tile=tile, **kwargs)
        self.out_traces = da.zeros((self.num_traces, self.num_samples), chunks=self.t.chunks)

    # @staticmethod    
    def auto_out_filename(self):
        base_name, ext = os.path.splitext(self.input_path)
        self.output_path = f"{base_name}_{self.__class__.__name__}{ext}"


if __name__ == "__main__":
    # 示例用法
    input_path = "E:\\codes\\template\\dataset\\20250221202721.zarr"
    testPP = PPBasic(input_path=input_path)
    testPP.auto_out_filename()
    print(testPP.output_path)
