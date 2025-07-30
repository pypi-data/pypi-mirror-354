import os
from typing import Union, Optional
import threading
from queue import Queue
import numpy as np

from simba.utils.read_write import get_video_meta_data


class AsyncVideoFrameReader():



    def __init__(self,
                 video_path: Union[str, os.PathLike],
                 batch_size: int = 100,
                 max_que_size: int = 2,
                 start_idx: Optional[int] = None,
                 end_idx: Optional[int] = None):

        video_meta_data = get_video_meta_data(video_path=video_path)
        self.start_idx = 0 if start_idx is None else start_idx
        self.end_idx = video_meta_data['frame_count'] if end_idx is None else end_idx
        self.frame_queue = Queue(maxsize=max_que_size)
        self.batch_size = batch_size


    def run(self):
        while self.start_idx < self.end_idx:
            self.end_idx = min(self.start_idx + self.batch_size, self.end_idx)
            print(f"[Reader] Loading frames {self.start_idx}-{self.end_idx}...")
            print(self.start_idx, self.end_idx)
            self.start_idx = self.end_idx






video_path = "/mnt/c/troubleshooting/RAT_NOR/project_folder/videos/03152021_NOB_IOT_8.mp4"
runner = AsyncVideoFrameReader(video_path=video_path)
runner.run()



