from typing import Optional

from virtual_world.organisms.position import PositionSquare, PositionHexagon


class OrganismFactory:
    import virtual_world.organisms.organism as organism

    @classmethod
    def create(
        cls, data: "organism.Organism.OrganismRepresentation"
    ) -> "organism.Organism":
        organism_type = data["type"]
        organism: "organism.Organism" | None = cls.create_base_organism(organism_type)  # type: ignore # name-defined

        if organism is not None:
            organism.set_from_dict(data)
            return organism  # type: ignore # no-any-return
        else:
            raise ValueError(f"Unknown organism type: {organism_type}")

    @staticmethod
    def create_base_organism(
        organism_type: str, position: Optional[PositionSquare | PositionHexagon] = None
    ) -> "organism.Organism":
        from virtual_world.organisms.animals import animals
        from virtual_world.organisms.plants import plants

        organism: "organism.Organism" | None = None  # type: ignore # name-defined

        if organism_type == "Wolf":
            organism = animals.Wolf()
        elif organism_type == "Sheep":
            organism = animals.Sheep()
        elif organism_type == "Turtle":
            organism = animals.Turtle()
        elif organism_type == "Fox":
            organism = animals.Fox()
        elif organism_type == "Antelope":
            organism = animals.Antelope()
        elif organism_type == "CyberSheep":
            organism = animals.CyberSheep()
        elif organism_type == "Grass":
            organism = plants.Grass()
        elif organism_type == "Dandelion":
            organism = plants.Dandelion()
        elif organism_type == "Guarana":
            organism = plants.Guarana()
        elif organism_type == "Belladonna":
            organism = plants.Belladonna()
        elif organism_type == "HeracleumSosnowskyi":
            organism = plants.HeracleumSosnowskyi()
        else:
            raise ValueError(f"Unknown organism type: {organism_type}")

        if position is not None:
            organism.set_position(position)

        return organism
