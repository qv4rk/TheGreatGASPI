"""
Metric calculation functions for The Great GASPI

Implements algorithms for computing topographic asymmetry, hydropolitics,
infrastructure control, and legal friction metrics.
"""

import math
import numpy as np
from typing import Tuple, Dict, List
from geopandas import GeoDataFrame
import geopandas as gpd


# ============================================================================
# PILLAR 1: TOPOGRAPHIC ASYMMETRY CALCULATIONS
# ============================================================================

def calculate_asymmetry_factor(gdf: GeoDataFrame) -> float:
    """
    Calculate Asymmetry Factor (AF)
    AF = (Ar / At) * 100
    Where:
        Ar = area of river/basin on right side of centerline
        At = total basin area
    Returns value between 0-100; 50 = symmetric
    """
    if gdf.empty:
        return 50.0  # Default symmetric

    try:
        total_area = gdf.geometry.area.sum()
        if total_area == 0:
            return 50.0

        # Calculate centerline
        bounds = gdf.total_bounds
        center_x = (bounds[0] + bounds[2]) / 2

        # Partition into right side
        right_mask = gdf.geometry.centroid.x >= center_x
        right_area = gdf[right_mask].geometry.area.sum()

        af = (right_area / total_area) * 100
        return float(af)
    except Exception:
        return 50.0


def calculate_transverse_symmetry(dem_array: np.ndarray, bounds: Tuple) -> float:
    """
    Calculate Transverse Symmetry Factor (T)
    T = Da / Dd
    Where:
        Da = mean distance from flow line to centerline
        Dd = mean distance from basin boundary to centerline
    Values closer to 0 indicate more symmetry
    """
    if dem_array is None or dem_array.size == 0:
        return 0.5  # Default moderate asymmetry

    try:
        # Simplified: use elevation std as proxy for asymmetry
        # In production, would use actual flow line analysis
        elevation_gradient = np.std(dem_array)
        max_elevation = np.max(dem_array)

        if max_elevation == 0:
            return 0.5

        t_factor = elevation_gradient / max_elevation
        return float(min(t_factor, 1.0))
    except Exception:
        return 0.5


def calculate_basin_elongation(gdf: GeoDataFrame) -> float:
    """
    Calculate Basin Elongation Ratio (Eb)
    Eb = sqrt(A / π) / L
    Where:
        A = basin area
        L = maximum length
    Values < 0.7 indicate tectonically active areas
    """
    if gdf.empty:
        return 0.75  # Default

    try:
        total_area = gdf.geometry.area.sum()
        bounds = gdf.total_bounds
        max_length = math.sqrt((bounds[2] - bounds[0])**2 + (bounds[3] - bounds[1])**2)

        if max_length == 0:
            return 0.75

        eb = (math.sqrt(total_area / math.pi)) / max_length
        return float(min(eb, 1.0))
    except Exception:
        return 0.75


def calculate_valley_floor_ratio(dem_array: np.ndarray) -> float:
    """
    Calculate Valley Floor Ratio (Vf)
    Vf = (valley_width) / ((left_elevation + right_elevation) / 2 - valley_floor_elevation)
    Low Vf (0.192-0.263) = V-shaped valley, indicates active uplift
    High Vf (>0.8) = flat-bottomed valley, indicates stable terrain
    """
    if dem_array is None or dem_array.size == 0:
        return 0.5  # Default

    try:
        # Simplified calculation
        min_elev = np.min(dem_array)
        max_elev = np.max(dem_array)
        mean_elev = np.mean(dem_array)

        elevation_range = max_elev - min_elev
        if elevation_range == 0:
            return 0.5

        # Vf proxy: ratio of mean to range
        vf = (mean_elev - min_elev) / elevation_range
        return float(vf)
    except Exception:
        return 0.5


def calculate_high_ground_advantage(
    dem_array: np.ndarray,
    territory_bounds: Dict,
    total_area_sqkm: float
) -> Dict:
    """
    Calculate high-ground tactical advantage metrics
    Returns:
        - elevation_advantage_m: relative elevation gain
        - viewshed_coverage_pct: visible terrain percentage
        - chokepoints_controlled: estimated bottleneck count
        - rating: 0-1 normalized advantage score
    """
    if dem_array is None or dem_array.size == 0:
        return {
            "elevation_advantage_m": 0,
            "viewshed_coverage_pct": 0,
            "chokepoints_controlled": 0,
            "rating": 0.0
        }

    try:
        min_elevation = float(np.min(dem_array))
        max_elevation = float(np.max(dem_array))
        elevation_advantage = max_elevation - min_elevation

        # Estimate viewshed: higher terrain sees more (proxy)
        mean_elevation = float(np.mean(dem_array))
        normalized_height = (mean_elevation - min_elevation) / (elevation_advantage + 1)
        viewshed_pct = min(100, normalized_height * 150)  # Scale to 0-100

        # Estimate chokepoints: valleys create bottlenecks
        # Simplified: count areas with high elevation gradient
        gradient = np.gradient(dem_array.flatten())
        high_gradient_pixels = np.sum(np.abs(gradient) > np.percentile(np.abs(gradient), 75))
        chokepoints = int(max(1, high_gradient_pixels / (len(gradient) / 10)))

        # Composite rating
        rating = min(1.0, (elevation_advantage / 1000) * 0.3 + (viewshed_pct / 100) * 0.4 + (chokepoints / 10) * 0.3)

        return {
            "elevation_advantage_m": elevation_advantage,
            "viewshed_coverage_pct": viewshed_pct,
            "chokepoints_controlled": chokepoints,
            "rating": float(rating)
        }
    except Exception:
        return {
            "elevation_advantage_m": 0,
            "viewshed_coverage_pct": 0,
            "chokepoints_controlled": 0,
            "rating": 0.0
        }


def calculate_encirclement_ratio(territory_gdf: GeoDataFrame, control_gdf: GeoDataFrame) -> float:
    """
    Calculate Encirclement Percentage
    What % of a 360° perimeter is surrounded by higher elevations or control zones
    Range: 0-100%, where 100 = completely encircled
    """
    if territory_gdf.empty or control_gdf.empty:
        return 0.0

    try:
        territory_boundary = territory_gdf.unary_union
        control_boundary = control_gdf.unary_union

        # Simplified: measure perimeter intersections
        intersection = territory_boundary.intersection(control_boundary)
        if intersection.is_empty:
            return 0.0

        intersection_length = intersection.length if hasattr(intersection, 'length') else 0
        territory_perimeter = territory_boundary.length

        if territory_perimeter == 0:
            return 0.0

        encirclement_pct = min(100, (intersection_length / territory_perimeter) * 100)
        return float(encirclement_pct)
    except Exception:
        return 0.0


# ============================================================================
# PILLAR 2: HYDROPOLITICS CALCULATIONS
# ============================================================================

def calculate_water_security_score(
    upstream_control: bool,
    dam_control_ratio: float,
    groundwater_access_pct: float,
    arable_land_pct: float,
    food_import_dependency_pct: float
) -> float:
    """
    Calculate composite Water Security Score (0-100)
    Factors:
        - Upstream positioning (40%)
        - Dam control ratio (30%)
        - Groundwater access (20%)
        - Food self-sufficiency (10%)
    """
    score = 0.0

    # Upstream advantage
    upstream_component = 40 if upstream_control else 0

    # Dam control (inverse of external control)
    dam_component = (1 - dam_control_ratio) * 30

    # Groundwater access
    groundwater_component = groundwater_access_pct * 20 / 100

    # Food self-sufficiency (inverse of import dependency)
    food_component = (100 - food_import_dependency_pct) * 10 / 100

    score = upstream_component + dam_component + groundwater_component + food_component
    return float(min(100, max(0, score)))


def calculate_resource_security_composite(
    water_security: float,
    agricultural_autonomy: float,
    energy_self_sufficiency_pct: float
) -> float:
    """
    Calculate composite Resource Security Score (0-100)
    Weighted average of water, food, and energy security
    """
    composite = (water_security * 0.4 + agricultural_autonomy * 0.3 + energy_self_sufficiency_pct * 0.3)
    return float(min(100, max(0, composite)))


# ============================================================================
# PILLAR 3: INFRASTRUCTURE CALCULATIONS
# ============================================================================

def calculate_infrastructural_control_score(
    airspace_external_control_pct: float,
    spectrum_external_bands: int,
    total_spectrum_bands: int,
    port_accessibility_ratio: float,
    border_checkpoint_density: float,
    permit_restrictiveness: int,
    currency_control_ratio: float,
    power_grid_self_sufficiency_pct: float
) -> float:
    """
    Calculate composite Infrastructural Control Score (0-100)
    Components:
        - Airspace (20%)
        - Spectrum/comms (20%)
        - Maritime/ports (15%)
        - Borders/mobility (20%)
        - Currency (15%)
        - Energy (10%)
    """
    score = 0.0

    # Airspace: inverse of external control
    airspace_component = (1 - airspace_external_control_pct / 100) * 20

    # Spectrum: ratio of autonomous bands
    spectrum_autonomous = max(0, total_spectrum_bands - spectrum_external_bands)
    spectrum_component = (spectrum_autonomous / max(1, total_spectrum_bands)) * 20

    # Maritime: port access ratio
    maritime_component = port_accessibility_ratio * 15

    # Borders: inverse of restrictiveness
    border_component = (1 - permit_restrictiveness / 10) * 20

    # Currency: autonomy ratio
    currency_component = (1 - currency_control_ratio / 100) * 15

    # Energy: self-sufficiency
    energy_component = power_grid_self_sufficiency_pct * 10 / 100

    score = airspace_component + spectrum_component + maritime_component + border_component + currency_component + energy_component
    return float(min(100, max(0, score)))


# ============================================================================
# PILLAR 4: LEGAL-CULTURAL FRICTION CALCULATIONS
# ============================================================================

def calculate_legal_friction_density(
    family_law_divergence: int,
    criminal_law_divergence: int,
    commercial_law_divergence: int,
    personal_status_divergence: int,
    population_affected: int,
    total_population: int
) -> float:
    """
    Calculate Legal Friction Density (0-100)
    Composite of statutory divergence metrics weighted by population exposure
    """
    avg_divergence = (family_law_divergence + criminal_law_divergence + commercial_law_divergence + personal_status_divergence) / 4.0
    friction_score = avg_divergence * 10  # Scale 1-10 to 10-100

    # Weight by population exposure
    population_ratio = population_affected / max(1, total_population)
    weighted_friction = friction_score * population_ratio + (100 - 100 * population_ratio) * 0.3

    return float(min(100, max(0, weighted_friction)))


def calculate_jurisdictional_autonomy_score(
    local_legislative_power_pct: float,
    external_veto_ratio: float,
    personal_status_local_control_pct: float,
    legal_friction_density: float
) -> float:
    """
    Calculate Jurisdictional Autonomy Score (0-100)
    Measures degree of local legal independence vs external veto
    """
    legislative_component = local_legislative_power_pct * 0.4
    veto_component = (1 - external_veto_ratio) * 100 * 0.3
    personal_status_component = personal_status_local_control_pct * 0.2
    friction_inverse_component = (100 - legal_friction_density) * 0.1

    score = legislative_component + veto_component + personal_status_component + friction_inverse_component
    return float(min(100, max(0, score)))


# ============================================================================
# COMPOSITE SOVEREIGNTY INDEX
# ============================================================================

def calculate_composite_sovereignty_index(
    jurisdictional_autonomy: float,
    resource_security: float,
    infrastructural_control: float,
    topographic_advantage_rating: float
) -> Tuple[float, Dict]:
    """
    Calculate final Composite GASPI Sovereignty Index (0-100)
    Weighted average of the four pillars
    Returns:
        - composite_score: 0-100
        - component_breakdown: Dict with individual components
    """
    # Weights: Jurisdictional 30%, Resource 25%, Infrastructure 25%, Geographic 20%
    composite = (
        jurisdictional_autonomy * 0.30 +
        resource_security * 0.25 +
        infrastructural_control * 0.25 +
        (topographic_advantage_rating * 100) * 0.20
    )

    component_breakdown = {
        "jurisdictional": jurisdictional_autonomy,
        "resource": resource_security,
        "infrastructure": infrastructural_control,
        "topographic": topographic_advantage_rating * 100
    }

    return float(min(100, max(0, composite))), component_breakdown


# ============================================================================
# BATCH CALCULATION ORCHESTRATOR
# ============================================================================

def calculate_all_metrics(
    territory_gdf: GeoDataFrame,
    dem_array: np.ndarray,
    hydrology_params: Dict,
    infrastructure_params: Dict,
    legal_params: Dict
) -> Dict:
    """
    Orchestrate all metric calculations for a territory
    Returns complete scorecard for database storage
    """
    # Pillar 1: Topography
    af = calculate_asymmetry_factor(territory_gdf)
    t = calculate_transverse_symmetry(dem_array, territory_gdf.total_bounds)
    eb = calculate_basin_elongation(territory_gdf)
    vf = calculate_valley_floor_ratio(dem_array)
    hg = calculate_high_ground_advantage(dem_array, {}, territory_gdf.geometry.area.sum())

    # Pillar 2: Hydrology
    water_score = calculate_water_security_score(**hydrology_params)
    resource_score = calculate_resource_security_composite(
        water_score,
        hydrology_params.get("agricultural_autonomy", 50),
        hydrology_params.get("energy_self_sufficiency_pct", 50)
    )

    # Pillar 3: Infrastructure
    infra_score = calculate_infrastructural_control_score(**infrastructure_params)

    # Pillar 4: Legal
    legal_friction = calculate_legal_friction_density(**legal_params)
    jurisdictional_score = calculate_jurisdictional_autonomy_score(
        local_legislative_power_pct=50,  # Default; should come from data
        external_veto_ratio=0.6,
        personal_status_local_control_pct=legal_params.get("personal_status_local_control", 40),
        legal_friction_density=legal_friction
    )

    # Composite
    composite, breakdown = calculate_composite_sovereignty_index(
        jurisdictional_score,
        resource_score,
        infra_score,
        hg["rating"]
    )

    return {
        "topographic": {
            "asymmetry_factor_AF": af,
            "transverse_symmetry_T": t,
            "basin_elongation_Eb": eb,
            "valley_floor_ratio_Vf": vf,
            "high_ground": hg
        },
        "hydrology": {
            "water_security_score": water_score,
            "resource_security_composite": resource_score
        },
        "infrastructure": {
            "infrastructural_control_score": infra_score
        },
        "legal": {
            "legal_friction_density": legal_friction,
            "jurisdictional_autonomy_score": jurisdictional_score
        },
        "composite": {
            "sovereignty_index": composite,
            "breakdown": breakdown
        }
    }
