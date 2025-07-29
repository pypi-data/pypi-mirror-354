

from typing import Optional

import math

import torch

from torchao.prototype.low_bit_optim.quant_utils import create_dynamic_map
from .linear_sr_2bit import LinearSROptimState2bit
from .utils import set_block_size

QMAP_SIGNED_DE = create_dynamic_map(signed=True, max_exponent_bits=1, total_bits=2)
QMAP_UNSIGNED_DE = create_dynamic_map(signed=False, max_exponent_bits=1, total_bits=2)


class DESROptimState2bit(LinearSROptimState2bit):

    @classmethod
    def zeros(cls, shape, signed: bool = True, block_size: int = 0, device=None, **other_kwargs):
        shape = (shape,) if isinstance(shape, int) else shape
        n_elems = math.prod(shape)
        block_size = set_block_size(n_elems, block_size)

        codes = torch.zeros(n_elems // 4, dtype=torch.uint8, device=device)
        scale = torch.zeros(n_elems // block_size, device=device)
        qmap = torch.tensor(QMAP_SIGNED_DE if signed else QMAP_UNSIGNED_DE, device=device)
        return cls(codes, scale, qmap, signed, shape)