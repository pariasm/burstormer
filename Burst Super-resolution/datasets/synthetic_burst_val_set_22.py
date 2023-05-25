import torch
import cv2
import numpy as np
import pickle as pkl


class SyntheticBurstVal(torch.utils.data.Dataset):
    """ Synthetic burst validation set. The validation burst have been generated using the same synthetic pipeline as
    employed in SyntheticBurst dataset.
    """
    def __init__(self, root):
        self.root = root
        self.burst_list = list(range(100))
        self.burst_size = 14

    def __len__(self):
        return len(self.burst_list)

    def _read_burst_image(self, index, image_id):
        im = cv2.imread('{}/{:04d}/im_raw_{:02d}.png'.format(self.root, index, image_id), cv2.IMREAD_UNCHANGED)
        im_t = torch.from_numpy(im.astype(np.float32)).permute(2, 0, 1).float() / (2**14)
        return im_t

    def _read_meta_info(self, index):
        with open('{}/{:04d}/meta_info.pkl'.format(self.root, index), "rb") as input_file:
            meta_info = pkl.load(input_file)

        return meta_info

    def __getitem__(self, index):
        """ Generates a synthetic burst
                args:
                    index: Index of the burst
                returns:
                    burst: LR RAW burst, a torch tensor of shape
                           [14, 4, 48, 48]
                           The 4 channels correspond to 'R', 'G', 'G', and 'B' values in the RGGB bayer mosaick.
                    meta_info: Meta information about the burst
                """
        burst_name = '{:04d}'.format(index)
        burst = [self._read_burst_image(index, i) for i in range(self.burst_size)]
        burst = torch.stack(burst, 0)

        meta_info = self._read_meta_info(index)
        meta_info['burst_name'] = burst_name

        return burst, meta_info