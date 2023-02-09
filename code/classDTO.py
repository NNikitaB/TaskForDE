from pydantic import BaseModel
from typing import List, Optional


class RocketDTO(BaseModel):
    name: str
    wikipedia: Optional[str]
    description: Optional[str]
    id: str


class MissionDTO(BaseModel):
    id: str
    name: str


class innerrocketDTO(BaseModel):
    id: str


class innerRocketDTO(BaseModel):
    #mission_id: List[str]
    rocket: innerrocketDTO


class LaunchDTO(BaseModel):
    class Rocket:
        class rocked:
            rocket_id: str
        mission_id: List[str]
    rocket: innerRocketDTO
    detail: Optional[str]
    mission_name: Optional[str]
    mission_id: List[str]
    launch_date_utc: str
    id :str


def my_parse_json_to_dto(d: dict):
    ls_m = []
    ls_r = []
    ls_l = []
    if 'missions' in d:
        for it in d['missions']:
            m = MissionDTO.parse_obj(it)
            ls_m.append(m)
    if 'rockets' in d:
        for it in d['rockets']:
            r = RocketDTO.parse_obj(it)
            ls_r.append(r)
    if 'launches' in d:
        for it in d['launches']:
            launch = LaunchDTO.parse_obj(it)
            ls_l.append(launch)
    return ls_m, ls_r, ls_l
