from dataclasses import dataclass
import random
import sys

sys.path.append('..')

from constants.enums import DistributionType


@dataclass
class MinMaxRandomValue:
    """
    Type of randomly generated value with a min and max.

    Attributes:
        min: The minimum value.
        max: The maximum value.
        distribution_type: The distribution type.
        distribution_params: The distribution parameters.
    """
    min: float
    max: float
    distribution_type: DistributionType
    distribution_params: dict[str, float]

    def get_random_value(self):
        match self.distribution_type:
            case DistributionType.UNIFORM:
                return random.uniform(self.min, self.max)
            case DistributionType.NORMAL:
                dist_value = random.normalvariate(self.distribution_params["avg"], self.distribution_params["stddev"])
                return min(self.max, max(self.min, dist_value))
            case DistributionType.EXPONENTIAL:
                dist_value = random.expovariate(self.distribution_params["lambda"])
                return min(self.max, max(self.min, dist_value))
            case _:
                raise ValueError("Unknown distribution type")
