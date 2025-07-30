"""
Expects the structure of the New Eden's universe changes seldom enough to
negate the regeneration of the spatial data on every request.

Can be used by a dev to regenerate the spatial files and update the static
cache prior ot publishing a new release.
"""

from shapely import MultiPoint
from shapely.geometry import mapping

from eveuniverse.models import EveConstellation, EveRegion, EveSolarSystem, EveStargate


class Geospatial:

    @staticmethod
    def layer(name: str):
        match name:
            case "solar_systems_points":
                return Geospatial.solar_systems_points()
            case "constellations_polygons":
                return Geospatial.constellations_polygons()
            case "regions_polygons":
                return Geospatial.regions_polygons()
            case "stargates_lines":
                return Geospatial.stargates_lines()

    @staticmethod
    def solar_systems_points():
        features = []
        for system in EveSolarSystem.objects.all():
            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [system.position_x, system.position_z],
                    },
                    "properties": {
                        "id": system.id,
                        "name": system.name,
                        "security_status": system.security_status,
                        "constellation_id": system.eve_constellation.id,
                        "constellation_name": system.eve_constellation.name,
                        "region_id": system.eve_constellation.eve_region.id,
                        "region_name": system.eve_constellation.eve_region.name,
                    },
                }
            )

        geojson = {"type": "FeatureCollection", "features": features}
        return geojson

    @staticmethod
    def constellations_polygons():
        constellations = {}
        for system in EveSolarSystem.objects.all():
            constellations.setdefault(system.eve_constellation.id, []).append(system)

        features = []
        for constellation_id, systems in constellations.items():
            points = [[system.position_x, system.position_z] for system in systems]
            if len(points) < 3:
                continue
            multipoint = MultiPoint(points)
            hull = multipoint.convex_hull
            constellation_name = EveConstellation.objects.get(id=constellation_id).name
            features.append(
                {
                    "type": "Feature",
                    "geometry": mapping(hull),
                    "properties": {
                        "constellation_id": constellation_id,
                        "constellation_name": constellation_name,
                    },
                }
            )

        geojson = {"type": "FeatureCollection", "features": features}
        return geojson

    @staticmethod
    def regions_polygons():
        regions = {}
        for system in EveSolarSystem.objects.all():
            regions.setdefault(system.eve_constellation.eve_region.id, []).append(
                system
            )

        features = []
        for region_id, systems in regions.items():
            points = [[system.position_x, system.position_z] for system in systems]
            if len(points) < 3:
                continue
            multipoint = MultiPoint(points)
            hull = multipoint.convex_hull
            region_name = EveRegion.objects.get(id=region_id).name
            features.append(
                {
                    "type": "Feature",
                    "geometry": mapping(hull),
                    "properties": {
                        "region_id": region_id,
                        "region_name": region_name,
                    },
                }
            )

        geojson = {"type": "FeatureCollection", "features": features}
        return geojson

    @staticmethod
    def stargates_lines():

        stargates = {}
        connections = []
        for gate in EveStargate.objects.all():
            stargates[gate.id] = {
                "name": f"{gate.eve_solar_system.name} > {gate.destination_eve_solar_system.name}",
                "coords": [
                    gate.eve_solar_system.position_x,
                    gate.eve_solar_system.position_z,
                ],
            }

            # Sometimes gate.destination_eve_stargate_id is null
            # When this happens, pick the first gate found for gate.destination_eve_solar_system
            desto_gate = gate.destination_eve_stargate_id
            if desto_gate is None:
                desto_gate = (
                    EveStargate.objects.filter(
                        eve_solar_system=gate.destination_eve_solar_system
                    )
                    .first()
                    .id
                )
            connections.append((gate.id, desto_gate))

        features = []
        for conn in connections:
            id1, id2 = conn
            if id2 is None:  # Some stargates go nowhere?
                continue
            sg1 = stargates[id1]
            sg2 = stargates[id2]
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [sg1["coords"], sg2["coords"]],
                },
                "properties": {"from": sg1["name"], "to": sg2["name"]},
            }
            features.append(feature)

        geojson = {"type": "FeatureCollection", "features": features}
        return geojson
