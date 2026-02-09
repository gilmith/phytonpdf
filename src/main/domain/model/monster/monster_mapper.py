from src.main.domain.model.monster.Monster import Monster
from src.main.infraestructure.documents.MonsterDocument import MonsterDocument

def monster_to_document(monster: Monster, _id: str = None) -> MonsterDocument:
    """
    Convierte una instancia de Monster a MonsterDocument.
    Si se proporciona _id, se utiliza; de lo contrario, se deja como None.
    """
    return MonsterDocument(
        _id=_id if _id is not None else '',
        name=monster.name,
        weather_land=monster.weather_land,
        frequency=monster.frequency,
        organization=monster.organization,
        activity_cycle=monster.activity_cycle,
        diet=monster.diet,
        intelligence=monster.intelligence,
        treasures=monster.treasures,
        alignment=monster.alignment,
        number_apparitions=monster.number_apparitions,
        armor_category=monster.armor_category,
        movement=monster.movement,
        hit_dice=monster.hit_dice,
        gac0=monster.gac0,
        attacks=monster.attacks,
        damage=monster.damage,
        special_attacks=monster.special_attacks,
        special_defenses=monster.special_defenses,
        magic_resistance=monster.magic_resistance,
        size=monster.size,
        morality=monster.morality,
        pe_value=monster.pe_value
    )

def document_to_monster(document: MonsterDocument) -> Monster:
    """
    Convierte una instancia de MonsterDocument a Monster (sin el campo _id).
    """
    return Monster(
        name=document.name,
        weather_land=document.weather_land,
        frequency=document.frequency,
        organization=document.organization,
        activity_cycle=document.activity_cycle,
        diet=document.diet,
        intelligence=document.intelligence,
        treasures=document.treasures,
        alignment=document.alignment,
        number_apparitions=document.number_apparitions,
        armor_category=document.armor_category,
        movement=document.movement,
        hit_dice=document.hit_dice,
        gac0=document.gac0,
        attacks=document.attacks,
        damage=document.damage,
        special_attacks=document.special_attacks,
        special_defenses=document.special_defenses,
        magic_resistance=document.magic_resistance,
        size=document.size,
        morality=document.morality,
        pe_value=document.pe_value
    )

