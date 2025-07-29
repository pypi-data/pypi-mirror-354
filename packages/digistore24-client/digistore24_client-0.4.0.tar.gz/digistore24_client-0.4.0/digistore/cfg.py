import dataclasses
import os

import dacite
import yaml

own_dir = os.path.dirname(__file__)


@dataclasses.dataclass
class DigistoreCfg:
    api_key: str


def config(
    path: str=None,
) -> DigistoreCfg:
    if not path:
        path = os.path.join(own_dir, '..', 'digistore-cfg.yaml')

    with open(path) as f:
        return dacite.from_dict(
            data_class=DigistoreCfg,
            data=yaml.safe_load(f),
        )
