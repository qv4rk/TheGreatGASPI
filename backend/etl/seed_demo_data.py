"""
Demo Data Populator for The Great GASPI
Populates spatial features, population density pockets, and other derived data
Run AFTER 002_seed_demo_data.sql has been applied
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from geoalchemy2 import func as geo_func
import json
from datetime import datetime

from app.schemas import (
    Territory, PopulationDensityPocket, SpatialFeature,
    BorderCheckpoint, PhysicalBarrier, RiverBasin
)
from app.config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DemoDataPopulator:
    """Populates demo data for testing"""

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.session = Session(self.engine)

    # ========================================================================
    # WEST BANK DEMO DATA
    # ========================================================================

    def populate_west_bank(self):
        """Populate West Bank with spatial features and demographics"""
        logger.info("Populating West Bank demo data...")

        territory = self.session.query(Territory).filter(
            Territory.territory_id == "west-bank"
        ).first()

        if not territory:
            logger.error("West Bank territory not found")
            return

        # Population density pockets
        density_pockets = [
            {"name": "Ramallah-Al Bireh", "lat": 31.945, "lng": 35.201, "density": 2850, "pop": 195000},
            {"name": "Gaza City", "lat": 31.516, "lng": 34.453, "density": 3200, "pop": 430000},
            {"name": "Hebron", "lat": 31.531, "lng": 35.207, "density": 1650, "pop": 210000},
            {"name": "Nablus", "lat": 32.224, "lng": 35.234, "density": 1450, "pop": 145000},
        ]

        for pocket in density_pockets:
            dp = PopulationDensityPocket(
                territory_id=territory.id,
                name=pocket["name"],
                density_per_sqkm=pocket["density"],
                population=pocket["pop"],
                geom=f"POINT({pocket['lng']} {pocket['lat']})"
            )
            self.session.add(dp)

        # Border checkpoints
        checkpoints = [
            {"name": "Allenby Bridge", "type": "land", "lat": 31.867, "lng": 35.451},
            {"name": "Rafah Crossing", "type": "land", "lat": 31.286, "lng": 34.249},
            {"name": "Ben Gurion Airport", "type": "air", "lat": 31.895, "lng": 35.215},
        ]

        for cp in checkpoints:
            checkpoint = BorderCheckpoint(
                territory_id=territory.id,
                name=cp["name"],
                checkpoint_type=cp["type"],
                control_status="external",
                permit_requirement=True,
                geom=f"POINT({cp['lng']} {cp['lat']})"
            )
            self.session.add(checkpoint)

        # Physical barriers (separation wall)
        barrier = PhysicalBarrier(
            territory_id=territory.id,
            type="manmade",
            description="Israeli separation barrier",
            length_km=712,
            impact_score=0.92,
            geom="LINESTRING(35.2 31.9, 35.5 32.1, 35.4 32.3)"
        )
        self.session.add(barrier)

        # River basins
        river = RiverBasin(
            territory_id=territory.id,
            river_name="Jordan River",
            upstream_position=False,
            downstream_dependence=True,
            flow_direction="S",
            average_discharge_m3_s=50.0,
            geom="LINESTRING(35.4 33.2, 35.45 32.5, 35.4 31.95)"
        )
        self.session.add(river)

        # Spatial features (accessible vs restricted areas)
        accessible = SpatialFeature(
            territory_id=territory.id,
            feature_type="accessible_area",
            access_status="accessible",
            elevation_m=450,
            geom="POLYGON((35.25 32.0, 35.35 32.0, 35.35 32.1, 35.25 32.1, 35.25 32.0))",
            properties={"name": "Area A", "governance": "Palestinian Authority"}
        )
        self.session.add(accessible)

        restricted = SpatialFeature(
            territory_id=territory.id,
            feature_type="restricted_area",
            access_status="restricted",
            elevation_m=650,
            geom="POLYGON((35.4 32.1, 35.5 32.1, 35.5 32.2, 35.4 32.2, 35.4 32.1))",
            properties={"name": "Settlement Zone", "governance": "Israeli"}
        )
        self.session.add(restricted)

        self.session.commit()
        logger.info("West Bank demo data populated")

    # ========================================================================
    # WESTERN SAHARA DEMO DATA
    # ========================================================================

    def populate_western_sahara(self):
        """Populate Western Sahara with spatial features"""
        logger.info("Populating Western Sahara demo data...")

        territory = self.session.query(Territory).filter(
            Territory.territory_id == "western-sahara"
        ).first()

        if not territory:
            logger.error("Western Sahara territory not found")
            return

        # Population centers
        density_pockets = [
            {"name": "Laayoune", "lat": 27.138, "lng": -13.202, "density": 450, "pop": 195000},
            {"name": "Dakhla", "lat": 23.656, "lng": -15.948, "density": 280, "pop": 95000},
        ]

        for pocket in density_pockets:
            dp = PopulationDensityPocket(
                territory_id=territory.id,
                name=pocket["name"],
                density_per_sqkm=pocket["density"],
                population=pocket["pop"],
                geom=f"POINT({pocket['lng']} {pocket['lat']})"
            )
            self.session.add(dp)

        # Checkpoints
        checkpoint = BorderCheckpoint(
            territory_id=territory.id,
            name="Laayoune Airport",
            checkpoint_type="air",
            control_status="external",
            permit_requirement=True,
            geom="POINT(-13.202 27.138)"
        )
        self.session.add(checkpoint)

        # Border wall (Moroccan berm)
        barrier = PhysicalBarrier(
            territory_id=territory.id,
            type="manmade",
            description="Moroccan defensive berm",
            length_km=2700,
            impact_score=0.88,
            geom="LINESTRING(-13.2 27.7, -13.2 21.4)"
        )
        self.session.add(barrier)

        self.session.commit()
        logger.info("Western Sahara demo data populated")

    # ========================================================================
    # NORTHERN CYPRUS DEMO DATA
    # ========================================================================

    def populate_northern_cyprus(self):
        """Populate Northern Cyprus with spatial features"""
        logger.info("Populating Northern Cyprus demo data...")

        territory = self.session.query(Territory).filter(
            Territory.territory_id == "northern-cyprus"
        ).first()

        if not territory:
            logger.error("Northern Cyprus territory not found")
            return

        # Major cities
        density_pockets = [
            {"name": "Nicosia (North)", "lat": 35.126, "lng": 33.383, "density": 1850, "pop": 145000},
            {"name": "Famagusta", "lat": 35.115, "lng": 33.947, "density": 950, "pop": 65000},
        ]

        for pocket in density_pockets:
            dp = PopulationDensityPocket(
                territory_id=territory.id,
                name=pocket["name"],
                density_per_sqkm=pocket["density"],
                population=pocket["pop"],
                geom=f"POINT({pocket['lng']} {pocket['lat']})"
            )
            self.session.add(dp)

        # Checkpoints
        checkpoint = BorderCheckpoint(
            territory_id=territory.id,
            name="Buffer Zone Crossing",
            checkpoint_type="land",
            control_status="disputed",
            permit_requirement=True,
            geom="POINT(33.383 35.126)"
        )
        self.session.add(checkpoint)

        # Green Line (buffer zone)
        barrier = PhysicalBarrier(
            territory_id=territory.id,
            type="manmade",
            description="UN Buffer Zone (Green Line)",
            length_km=180,
            impact_score=0.95,
            geom="LINESTRING(33.3 35.1, 33.9 35.5)"
        )
        self.session.add(barrier)

        self.session.commit()
        logger.info("Northern Cyprus demo data populated")

    # ========================================================================
    # TRANSNISTRIA DEMO DATA
    # ========================================================================

    def populate_transnistria(self):
        """Populate Transnistria with spatial features"""
        logger.info("Populating Transnistria demo data...")

        territory = self.session.query(Territory).filter(
            Territory.territory_id == "transnistria"
        ).first()

        if not territory:
            logger.error("Transnistria territory not found")
            return

        # Major cities
        density_pockets = [
            {"name": "Tiraspol", "lat": 47.485, "lng": 29.108, "density": 1250, "pop": 135000},
            {"name": "Bendery", "lat": 46.822, "lng": 29.475, "density": 850, "pop": 95000},
        ]

        for pocket in density_pockets:
            dp = PopulationDensityPocket(
                territory_id=territory.id,
                name=pocket["name"],
                density_per_sqkm=pocket["density"],
                population=pocket["pop"],
                geom=f"POINT({pocket['lng']} {pocket['lat']})"
            )
            self.session.add(dp)

        # Checkpoints (Dniester River crossings)
        checkpoints = [
            {"name": "Bendery Crossing", "type": "land", "lat": 46.822, "lng": 29.475},
            {"name": "Rybnitsa Crossing", "type": "land", "lat": 47.735, "lng": 29.639},
        ]

        for cp in checkpoints:
            checkpoint = BorderCheckpoint(
                territory_id=territory.id,
                name=cp["name"],
                checkpoint_type=cp["type"],
                control_status="external",
                permit_requirement=True,
                geom=f"POINT({cp['lng']} {cp['lat']})"
            )
            self.session.add(checkpoint)

        # Dniester River border
        river = RiverBasin(
            territory_id=territory.id,
            river_name="Dniester River",
            upstream_position=False,
            downstream_dependence=False,
            flow_direction="SE",
            average_discharge_m3_s=238.0,
            geom="LINESTRING(29.0 48.8, 29.5 47.5, 29.6 46.3)"
        )
        self.session.add(river)

        self.session.commit()
        logger.info("Transnistria demo data populated")

    # ========================================================================
    # ORCHESTRATION
    # ========================================================================

    def populate_all(self):
        """Populate all demo data"""
        try:
            logger.info("Starting demo data population...")
            self.populate_west_bank()
            self.populate_western_sahara()
            self.populate_northern_cyprus()
            self.populate_transnistria()
            logger.info("✅ Demo data population complete!")
        except Exception as e:
            logger.error(f"Error populating demo data: {e}", exc_info=True)
            self.session.rollback()
            raise
        finally:
            self.session.close()


if __name__ == "__main__":
    populator = DemoDataPopulator(settings.database_url)
    populator.populate_all()
