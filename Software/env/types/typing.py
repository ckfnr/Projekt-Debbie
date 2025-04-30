from typing import TypeVar, TypedDict

# TypedDicts for the structure
class ChannelsDict(TypedDict):
    thigh: int
    lower_leg: int
    side_axis: int

class AnglesDict(TypedDict):
    min_thigh: int
    max_thigh: int
    min_lower_leg: int
    max_lower_leg: int
    min_side_axis: int
    max_side_axis: int

class DeviationsDict(TypedDict):
    thigh: int
    lower_leg: int
    side_axis: int

class MirroredDict(TypedDict):
    thigh: bool
    lower_leg: bool
    side_axis: bool

class LegConfigDict(TypedDict):
    channels: ChannelsDict
    angles: AnglesDict
    deviations: DeviationsDict
    mirrored: MirroredDict

ITER = TypeVar('ITER')
