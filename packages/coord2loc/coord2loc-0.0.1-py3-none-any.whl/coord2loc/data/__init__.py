import zlib
from importlib import resources
from typing import List

import msgpack
from shapely import Polygon, STRtree, from_wkb

DELIMITER = b"\x00\x00\x00\x00"
MSGPACK_POLYGONS = resources.files("coord2loc.data").joinpath("polygons.msgpack")
MSGPACK_META = resources.files("coord2loc.data").joinpath("meta.msgpack")


def load_polygons() -> List[Polygon]:
    polygons = []
    polygon_wkbs = msgpack.unpackb(
        zlib.decompress(MSGPACK_POLYGONS.read_bytes()), raw=False
    )
    print(f"Loaded {len(polygon_wkbs)} polygons")

    for wkb_bytes in polygon_wkbs:
        wkb_bytes = wkb_bytes.strip()
        if not wkb_bytes:
            continue
        polygons.append(from_wkb(wkb_bytes))

    return polygons


def load_meta() -> List[dict]:
    return msgpack.unpackb(zlib.decompress(MSGPACK_META.read_bytes()), raw=False)


def load() -> tuple[STRtree, List[Polygon], List[dict]]:
    polygons = load_polygons()
    meta = load_meta()
    assert len(polygons) == len(meta)

    return STRtree(polygons), polygons, meta
