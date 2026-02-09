from pydantic import BaseModel, Field

class MonsterDocument(BaseModel):
    _id: str
    name: str
    weather_land: str
    frequency: str
    organization: str
    activity_cycle: str
    diet: str
    intelligence: str
    treasures: str
    alignment: str
    number_apparitions: str
    armor_category: int
    movement: int
    hit_dice: int
    gac0: int
    attacks: int
    damage: str
    special_attacks: str
    special_defenses: str
    magic_resistance: str
    size: str
    morality: str
    pe_value: str

