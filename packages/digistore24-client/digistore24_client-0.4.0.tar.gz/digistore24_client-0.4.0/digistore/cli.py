#!/usr/bin/env python

import argparse
import os
import pprint
import sys


# make sure digistore package is available from PYTHONPATH
if os.path.islink(__file__):
    real_dir = os.path.dirname(os.path.realpath(__file__))
else:
    real_dir = os.path.dirname(__file__)

sys.path.insert(
    0,
    os.path.join(real_dir, '..'),
)

import digistore.cfg
import digistore.client


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cfg', default=None)
    parser.add_argument('url', nargs=1)

    parsed = parser.parse_args()

    cfg = digistore.cfg.config(path=parsed.cfg)
    client = digistore.client.DigistoreClient(
        api_key=cfg.api_key,
    )

    url = client.routes._url(parsed.url[0])

    resp = client.sess.get(url)

    if not resp.ok:
        print(f'Error {resp}')
        #print(resp.text)
        exit(1)

    pprint.pprint(resp.json())


if __name__ == '__main__':
    main()
