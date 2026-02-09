from beanie import Document
from typing import Optional

class MonsterBeanie(Document):
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

    class Settings:
        name = "monsters"

    @classmethod
    async def get_by_id(cls, _id: str) -> Optional["MonsterBeanie"]:
        return await cls.get(id)

    @classmethod
    async def get_by_name(cls, name: str) -> Optional["MonsterBeanie"]:
        return await cls.find_one(cls.name == name)

    async def save_monster(self) -> "MonsterBeanie":
        return await self.save()

    @classmethod
    async def delete_by_id(cls, _id: str) -> bool:
        monster = await cls.get(id)
        if monster:
            await monster.delete()
            return True
        return False

