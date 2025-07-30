# HA Synthetic Sensors

[![GitHub Release](https://img.shields.io/github/v/release/SpanPanel/ha-synthetic-sensors?style=flat-square)](https://github.com/SpanPanel/ha-synthetic-sensors/releases)
[![PyPI Version](https://img.shields.io/pypi/v/ha-synthetic-sensors?style=flat-square)](https://pypi.org/project/ha-synthetic-sensors/)
[![Python Version](https://img.shields.io/pypi/pyversions/ha-synthetic-sensors?style=flat-square)](https://pypi.org/project/ha-synthetic-sensors/)
[![License](https://img.shields.io/github/license/SpanPanel/ha-synthetic-sensors?style=flat-square)](https://github.com/SpanPanel/ha-synthetic-sensors/blob/main/LICENSE)

[![CI Status](https://img.shields.io/github/actions/workflow/status/SpanPanel/ha-synthetic-sensors/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/SpanPanel/ha-synthetic-sensors/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/SpanPanel/ha-synthetic-sensors?style=flat-square)](https://codecov.io/gh/SpanPanel/ha-synthetic-sensors)
[![Code Quality](https://img.shields.io/codefactor/grade/github/SpanPanel/ha-synthetic-sensors?style=flat-square)](https://www.codefactor.io/repository/github/spanpanel/ha-synthetic-sensors)
[![Security](https://img.shields.io/snyk/vulnerabilities/github/SpanPanel/ha-synthetic-sensors?style=flat-square)](https://snyk.io/test/github/SpanPanel/ha-synthetic-sensors)

[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![Type Checking: MyPy](https://img.shields.io/badge/type%20checking-mypy-blue?style=flat-square)](https://mypy-lang.org/)

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20development-FFDD00?style=flat-square&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/cayossarian)

A Python package for creating formula-based sensors in Home Assistant integrations using YAML configuration.

## What it does

- Creates Home Assistant sensor entities from mathematical formulas
- Evaluates math expressions using `simpleeval` library
- Maps variable names to Home Assistant entity IDs
- Manages sensor lifecycle (creation, updates, removal)
- Provides Home Assistant services for configuration management
- Tracks dependencies between sensors
- Caches formula results
- Variable declarations for shortcut annotations in math formulas
- Dynamic entity aggregation (regex, tags, areas, device_class patterns)
- Dot notation for entity attribute access

## Installation

```bash
pip install ha-synthetic-sensors
```

Development setup:

```bash
git clone https://github.com/SpanPanel/ha-synthetic-sensors
cd ha-synthetic-sensors
poetry install --with dev
```

**Key benefits of device integration:**

- **Unified Device View**: Synthetic sensors appear under your integration's device in HA UI
- **Lifecycle Control**: Parent integration controls setup, reload, and teardown
- **Update Coordination**: Synthetic sensors update within parent's async update routines
- **Entity Naming**: Sensors use parent integration's naming conventions and prefixes
- **Resource Sharing**: Parent can provide its own HA dependencies (hass, coordinators, etc.)

## YAML configuration

### Simple calculated sensors

```yaml
version: "1.0"

sensors:
  # Single formula sensor (90% of use cases)
  energy_cost_current:
    name: "Current Energy Cost"
    formula: "current_power * electricity_rate / 1000"
    variables:
      current_power: "sensor.span_panel_instantaneous_power"
      electricity_rate: "input_number.electricity_rate_cents_kwh"
    unit_of_measurement: "¢/h"
    state_class: "measurement"

  # Another simple sensor
  solar_sold_power:
    name: "Solar Sold Power"
    formula: "abs(min(grid_power, 0))"
    variables:
      grid_power: "sensor.span_panel_current_power"
    unit_of_measurement: "W"
    device_class: "power"
    state_class: "measurement"
```

### Rich sensors with calculated attributes

```yaml
sensors:
  # Sensor with calculated attributes
  energy_cost_analysis:
    name: "Energy Cost Analysis"
    formula: "current_power * electricity_rate / 1000"
    attributes:
      daily_projected:
        formula: "state * 24" # ref by main state alias
        unit_of_measurement: "¢"
      monthly_projected:
        formula: "energy_cost_analysis * 24 * 30" # ref by main sensor key
        unit_of_measurement: "¢"
      annual_projected:
        formula: "sensor.syn2_energy_cost_analysis * 24 * 365" # ref by entity_id
        unit_of_measurement: "¢"
      battery_efficiency:
        formula: "current_power * device.battery_level / 100" # using attribute access
        variables:
          device: "sensor.backup_device"
        unit_of_measurement: "W"
      efficiency:
        formula: "state / sensor.max_power_capacity * 100"
        unit_of_measurement: "%"
    variables:
      current_power: "sensor.span_panel_instantaneous_power"
      electricity_rate: "input_number.electricity_rate_cents_kwh"
    unit_of_measurement: "¢/h"
    device_class: "monetary"
    state_class: "measurement"
```

**How attributes work:**

- Main sensor state is calculated first using the `formula`
- Attributes are calculated second and have access to the `state` variable
- `state` always refers to the fresh main sensor calculation
- Attributes can also reference other entities normally (like `sensor.max_power_capacity` above)
- Each attribute shows up as `sensor.energy_cost_analysis.daily_projected` etc. in HA

## Entity Reference Patterns

The package supports multiple ways to reference entities in formulas:

### Filtered vs Unfiltered Collection Patterns

**Filtered patterns** first identify entities by a specific criteria, then aggregate their values:

- `device_class:`, `area:`, `tags:`, `regex:` - Filter entities first, then sum/count/average their states
- Use these when you want to aggregate entities of a specific type or location

**Unfiltered patterns** search across ALL entities in Home Assistant:

- `attribute:` - Searches every entity for matching attribute conditions
- `state:` - Searches every entity for matching state conditions
- Use these when you need broad searches across your entire system

**Targeted filtering** combines both approaches:

- `variable.attribute` - First filter by collection pattern, then check attributes on those entities
- Example: `battery_devices.battery_level<20` where `battery_devices: "device_class:battery"`

| Pattern                                     | Syntax                          | Example                                | Use Case                               |
| ------------------------------------------- | ------------------------------- | -------------------------------------- | -------------------------------------- |
| **Direct Entity ID**                        | `sensor.entity_name`            | `sensor.power_meter`                   | Quick references, cross-sensor         |
| **Reusable Variable Alias' to states**      | `variable_name`                 | `power_meter`                          | Most common, clean formulas            |
| **Sensor Key Reference**                    | `sensor_key`                    | `energy_analysis`                      | Reference other synthetic sensors      |
| **Sensor State Alias in attrubte formulas** | `state`                         | `state * 24`                           | In attributes, reference main sensor   |
| **Attribute Dot Notation**                  | `entity.attribute`              | `sensor1.battery_level`                | Access entity attributes               |
| **Sensor Collection Functions**             | `mathFunc(pattern:value)`       | `sum(regex:circuit_pattern)`           | Aggregate multiple entities by pattern |
| **Device Class Collection Math**            | `mathFunc(device_class:type)`   | `avg(device_class:temperature)`        | Aggregate by device type               |
| **Tag/Label Collection Math**               | `mathFunc(tags:tag1,tag2)`      | `count(tags:critical,important)`       | Aggregate by entity tags               |
| **Area Collection Math**                    | `mathFunc(area:location)`       | `sum(area:kitchen device_class:power)` | Aggregate by physical location         |
| **Attribute Collection Math**               | `mathFunc(attribute:condition)` | `count(attribute:battery_level<20)`    | Aggregate by attribute values          |
| **State Collection Math**                   | `mathFunc(state:condition)`     | `count(state:>100\|=on)`               | Aggregate by entity state values       |

### Variable Purpose and Scope

A variable serves as a short alias for the sensor or filter that it references.

Once defined a variable can be used in any formula whether in the main sensor state formula or attribute formula.

Attribute formulas automatically inherit all variables from their parent sensor:

```yaml
sensors:
  energy_analysis:
    name: "Energy Analysis"
    formula: "grid_power + solar_power"
    variables:
      grid_power: "sensor.grid_meter"
      solar_power: "sensor.solar_inverter"
      efficiency_factor: "input_number.base_efficiency"
      battery_devices: "device_class:battery"
    attributes:
      daily_projection:
        formula: "energy_analysis * 24" # References main sensor by key
      efficiency_percent:
        formula: "solar_power / (grid_power + solar_power) * 100" # Uses inherited variables
      low_battery_count:
        formula: "count(battery_devices.battery_level<20)" # Uses collection variable with dot notation
        unit_of_measurement: "devices"
    unit_of_measurement: "W"
    device_class: "power"
    state_class: "measurement"
```

### Collection Functions (Entity Aggregation)

Sum, average, or count entities dynamically using collection patterns:

```yaml
sensors:
  # State filtering across all entities
  high_power_or_active:
    name: "High Power or Active States"
    formula: count("state:>100|=on")
    unit_of_measurement: "count"

  # Device Class Collection
  count_open_doors_windows:
    name: "Open Doors and Windows"
    formula: sum("device_class:door|window")
    unit_of_measurement: "count"

  # Area-based aggregation
  garage_sensors:
    name: "Garage Sensors"
    formula: sum("area:garage|basement")
    unit_of_measurement: "count"

  # Tag-based aggregation
  critical_sensors:
    name: "Critical Sensors Active"
    formula: count("tags:critical|important")
    unit_of_measurement: "count"

  # Regex patterns
  total_circuit_power:
    name: "Total Circuit Power"
    formula: sum("regex:circuit_pattern")
    variables:
    # Pattern must be in input_text or input_text in variable
    circuit_pattern: "input_text.circuit_regex_pattern"
    unit_of_measurement: "W"
    device_class: "power"
    state_class: "measurement"

  # Attribute filtering across all entities
  low_battery_attributes:
    name: "Low Battery Attributes"
    formula: count("attribute:battery_level<20")
    unit_of_measurement: "count"

  # Attribute filtering by device class
  low_battery_devices:
    name: "Low Battery Devices"
    formula: count("device_class_var.battery_level<20")
    unit_of_measurement: "count"
    variables:
      device_class_var: "device_class:battery"

  # Mixed patterns in one formula
  comprehensive_analysis:
    name: "Comprehensive Power Analysis"
    formula: 'base_load + sum("regex:circuit_pattern") + backup_power.current_power'
    unit_of_measurement: "W"
    variables:
      base_load: "sensor.main_panel_power"
      circuit_pattern: "input_text.circuit_regex_pattern"
      backup_power: "sensor.backup_generator"
    device_class: "power"
    state_class: "measurement"
```

**Aggregate Collection Patterns**

```yaml
# Aggregate device class monitoring
sensors:
  dynamic_device_analysis:
    name: "Dynamic Device Analysis"
    formula: sum("device_class:device_type")
    variables:
      device_type: "input_select.monitoring_device_class"  # "temperature"
    unit_of_measurement: "°F"
    device_class: power
    state_class: "measurement

  regex_based_aggregate
    name: "Regex-Based Aggregate"
    formula: sum("regex:pattern_name")
    variables:
      pattern_name: input_text.the_regex    # The regex must use an input_text to hold it's state
    device_class: power
    state_class: "measurement

  # Use an attribute of the battery entities called battery_level
  power_to_battery_ratio:
    name: "Power to Battery Efficiency"
    formula: 'sum("device_class:power_type") / count(battery_class.battery_level > min_battery)'
    variables:
      power_type: "input_select.power_device_class"
      min_battery: "input_number.minimum_battery_level"
      battery_class: "device_class:battery"
    unit_of_measurement: W
    device_class: power
    state_class: "measurement

  sum_regex_patterns:
    name: "Sum Regex Patterns"
    formula: 'sum("regex:circuit_pattern", "regex:kitchen_pattern")'
    variables:
      circuit_pattern: "input_text.circuit_regex_pattern"
      kitchen_pattern: "input_text.kitchen_regex_pattern"
    unit_of_measurement: "W"
    device_class: "power"
    state_class: "measurement"
```

**Aggregation Functions Available:**

- `sum()` - Sum all matching entity values
- `avg()` / `mean()` - Average of all matching entities
- `count()` - Count of matching entities
- `min()` / `max()` - Minimum/maximum value
- `std()` / `var()` - Standard deviation/variance

**Collection Patterns:**

- `"device_class:power"` - Entities with specific device class
- `"regex:input_text.pattern"` - Entities matching regex pattern from variable
- `"area:kitchen"` - Entities in specific area
- `"tags:tag1,tag2"` - Entities with any of the specified tags
- `"attribute:battery_level<50"` - Entities with attribute conditions
- `"state:>100"` - Entities with state conditions

**Dynamic Patterns (Variable Substitution):**

- `"device_class:device_type"` - Variable substitution within patterns
- `"area:target_area"` - Dynamic area selection
- `"regex:pattern_variable"` - Aggregate regex patterns from variables

### OR Pattern Support (Pipe Syntax)

All collection patterns support OR logic using pipe (`|`) syntax for combining multiple conditions:

```yaml
sensors:
  # Device class OR patterns
  security_monitoring:
    name: "Security Device Count"
    formula: count("device_class:door|window|lock")
    unit_of_measurement: "devices"

  # Area OR patterns
  main_floor_power:
    name: "Main Floor Power"
    formula: sum("area:living_room|kitchen|dining_room")
    unit_of_measurement: "W"

  # Tag OR patterns
  critical_sensors:
    name: "Critical Sensors"
    formula: count("tags:critical|important|warning")
    unit_of_measurement: "devices"

  # Attribute OR patterns
  low_battery_or_offline:
    name: "Low Battery or Offline Devices"
    formula: count("attribute:battery_level<20|online=false")
    unit_of_measurement: "devices"

  # State OR patterns
  high_value_or_active:
    name: "High Value or Active States"
    formula: count("state:>100|=on")
    unit_of_measurement: "entities"

  # Regex OR patterns
  circuit_monitoring:
    name: "Circuit Power Monitoring"
    formula: sum("regex:circuit_pattern|kitchen_pattern")
    variables:
      circuit_pattern: "input_text.circuit_regex"
      kitchen_pattern: "input_text.kitchen_regex"
    unit_of_measurement: "W"
    device_class: "power"

  # Variable-based OR patterns
  dynamic_device_monitoring:
    name: "Dynamic Device Monitoring"
    formula: count("device_class:primary_type|secondary_type")
    variables:
      primary_type: "input_select.primary_device_class"
      secondary_type: "input_select.secondary_device_class"
    unit_of_measurement: "devices"

  # Complex formula with multiple OR patterns
  comprehensive_analysis:
    name: "Comprehensive Analysis"
    formula: 'sum("device_class:power|energy") + count("area:upstairs|downstairs") + avg("tags:monitor|alert")'
    unit_of_measurement: "mixed"
```

**OR Pattern Rules:**

- Use pipe (`|`) to separate multiple conditions: `door|window|lock`
- Supported across all pattern types: device_class, area, tags, regex, attribute, state
- Can mix variables and direct entity IDs: `variable_name|entity.direct_id`
- Regex patterns must reference `input_text` entities that contain the regex
- Supports any number of OR conditions: `condition1|condition2|condition3|condition4`

## Formula examples

```python
# Basic arithmetic
"circuit_1 + circuit_2 + circuit_3"

# Conditional logic
"net_power * buy_rate / 1000 if net_power > 0 else abs(net_power) * sell_rate / 1000"

# Mathematical functions
"abs(min(grid_power, 0))"                    # Absolute value, min/max
"sqrt(power_a**2 + power_b**2)"              # Square root, exponents
"round(temperature, 1)"                      # Rounding
"clamp(efficiency, 0, 100)"                  # Constrain to range
"map(brightness, 0, 255, 0, 100)"            # Map from one range to another
"avg(temp1, temp2, temp3)"                   # Average of values
"percent(used_space, total_space)"           # Percentage calculation

# Collection functions (entity aggregation)
sum("regex:circuit_pattern")                # Sum entities matching regex pattern from variable
sum("regex:pattern_variable")               # Sum entities using dynamic regex from variable
avg("device_class:temperature")             # Average all temperature sensors (static pattern)
count("tags:critical")                      # Count entities with 'critical' tag (static pattern)

# OR patterns in collection functions
count("device_class:door|window")           # Count all door OR window entities
sum("device_class:power|energy")            # Sum all power OR energy entities
avg("device_class:temperature|humidity")    # Average all temperature OR humidity entities
sum("regex:circuit_pattern|kitchen_pattern") # Sum entities matching multiple regex patterns

# Dot notation attribute access
"sensor1.battery_level + sensor2.battery_level"
"climate.living_room.current_temperature"

# Sensor references (by entity ID)
"sensor.syn2_hvac_total_power + sensor.syn2_lighting_total_power"
```

**Available Mathematical Functions:**

- Basic: `abs()`, `round()`, `floor()`, `ceil()`
- Math: `sqrt()`, `pow()`, `sin()`, `cos()`, `tan()`, `log()`, `exp()`
- Statistics: `min()`, `max()`, `avg()`, `mean()`, `sum()`
- Utilities: `clamp(value, min, max)`, `map(value, in_min, in_max, out_min, out_max)`, `percent(part, whole)`

## Why use this instead of templates?

While Home Assistant templates can create calculated sensors, this package provides much cleaner syntax for mathematical
operations and bulk sensor management.

### Syntax comparison

**This package:**

```yaml
formula: "net_power * buy_rate / 1000 if net_power > 0 else abs(net_power) * sell_rate / 1000"
variables:
  net_power: "sensor.span_panel_net_power"
  buy_rate: "input_number.electricity_buy_rate"
  sell_rate: "input_number.electricity_sell_rate"
```

**Template equivalent:**

```yaml
value_template: >
  {% set net_power = states('sensor.span_panel_net_power')|float %}
  {% set buy_rate = states('input_number.electricity_buy_rate')|float %}
  {% set sell_rate = states('input_number.electricity_sell_rate')|float %}
  {% if net_power > 0 %}
    {{ net_power * buy_rate / 1000 }}
  {% else %}
    {{ (net_power|abs) * sell_rate / 1000 }}
  {% endif %}
```

### Complex mathematics

**This package:**

```yaml
formula: "sqrt(power_a**2 + power_b**2 + power_c**2) * efficiency_factor"
```

**Template equivalent:**

```yaml
value_template: >
  {% set power_a = states('sensor.power_a')|float %}
  {% set power_b = states('sensor.power_b')|float %}
  {% set power_c = states('sensor.power_c')|float %}
  {% set efficiency_factor = states('input_number.efficiency_factor')|float %}
  {{ (power_a**2 + power_b**2 + power_c**2)**0.5 * efficiency_factor }}
```

### Variable reuse

**This package:**

```yaml
# Base calculation sensor
base_calculation:
  formula: "power_usage * rate"
  variables:
    power_usage: "sensor.power_meter"
    rate: "input_number.electricity_rate"

# Derived calculation referencing the first sensor
with_tax:
  formula: "sensor.syn2_base_calculation * 1.08"

# Or use attributes for related calculations
comprehensive_analysis:
  formula: "power_usage * rate"
  attributes:
    with_tax:
      formula: "state * 1.08"
    with_discount:
      formula: "state * 0.90"
  variables:
    power_usage: "sensor.power_meter"
    rate: "input_number.electricity_rate"
```

**Templates:** Each sensor needs separate template with repeated calculations.

### Bulk sensor management

**This package:** Single YAML file defines dozens of related sensors with shared variables and automatic dependency management.

**Templates:** Each sensor requires separate configuration entry with manual entity ID management.

## Home Assistant services

The package registers these services automatically:

```yaml
# Reload configuration
service: synthetic_sensors.reload_config

# Get sensor information
service: synthetic_sensors.get_sensor_info
data:
  entity_id: "sensor.syn2_energy_cost_analysis_current_cost_rate"

# Update sensor configuration
service: synthetic_sensors.update_sensor
data:
  entity_id: "sensor.syn2_energy_cost_analysis_current_cost_rate"
  formula: "updated_formula"

# Evaluate formula for testing
service: synthetic_sensors.evaluate_formula
data:
  formula: "A + B * 2"
  context:
    A: 10
    B: 5
```

## Manual component setup

```python
from ha_synthetic_sensors import (
    ConfigManager,
    Evaluator,
    NameResolver,
    SensorManager,
    ServiceLayer
)

# Initialize components
config_manager = ConfigManager(hass)
name_resolver = NameResolver(hass, variables=variables)
evaluator = Evaluator(hass)
sensor_manager = SensorManager(hass, name_resolver, async_add_entities)
service_layer = ServiceLayer(
    hass, config_manager, sensor_manager, name_resolver, evaluator
)

# Load configuration
config = config_manager.load_from_file("config.yaml")
await sensor_manager.load_configuration(config)

# Set up services
await service_layer.async_setup_services()
```

## Type safety

The package uses TypedDict for all data structures to provide type safety and better IDE support:

```python
from ha_synthetic_sensors.config_manager import FormulaConfigDict, SensorConfigDict
from ha_synthetic_sensors.evaluator import EvaluationResult
from ha_synthetic_sensors.service_layer import ServiceResponseData

# Configuration validation with types
validation_result = validate_yaml_content(yaml_content)
if validation_result["is_valid"]:
    sensors_count = validation_result["sensors_count"]
    formulas_count = validation_result["formulas_count"]

# Formula evaluation with typed results
result = evaluator.evaluate_formula(formula_config)
if result["success"]:
    value = result["value"]
else:
    error = result["error"]

# Integration status checking
status = integration.get_integration_status()
sensors_active = status["sensors_count"]
services_running = status["services_registered"]
```

Available TypedDict interfaces:

- `FormulaConfigDict`, `SensorConfigDict`, `ConfigDict` - Configuration structures
- `EvaluationResult`, `CacheStats`, `DependencyValidation` - Evaluator results
- `ServiceResponseData`, `EvaluationResponseData` - Service responses
- `EntityCreationResult`, `ValidationResult` - Entity factory results
- `VariableValidationResult`, `FormulaDependencies` - Name resolver results
- `IntegrationSetupResult`, `IntegrationStatus` - Integration management

## Configuration file format

Required fields:

- `formula`: Mathematical expression

Recommended fields:

- `name`: Display name for the sensor
- `device_class`: Home Assistant device class
- `state_class`: State class for statistics
- `unit_of_measurement`: Units for the result

Optional fields:

- `variables`: Map variable names to entity IDs
- `attributes`: Calculated attributes
- `enabled`: Whether this sensor is enabled
- `icon`: Icon for the entity

## Auto-configuration

The package automatically loads configuration files from these locations:

- `<config>/synthetic_sensors_config.yaml`
- `<config>/synthetic_sensors.yaml`
- `<config>/syn2_config.yaml`
- `<config>/syn2.yaml`

## Entity ID generation

Sensors create entities with predictable IDs:

- Sensor entities: `sensor.syn2_{sensor_key}`

## Integration Setup

### Standalone Integration

For a dedicated synthetic sensors integration:

```python
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ha_synthetic_sensors import async_setup_integration

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> bool:
    return await async_setup_integration(
        hass, config_entry, async_add_entities
    )
```

### Custom Integration Device Integration

For custom integrations that want synthetic sensors to appear under their device and be managed by their lifecycle:

```python
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo

from ha_synthetic_sensors.integration import SyntheticSensorsIntegration

class MyCustomIntegration:
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        self.hass = hass
        self.config_entry = config_entry
        self.sensor_manager = None

        # Define device info for this integration
        self.device_info = DeviceInfo(
            identifiers={("my_integration", "device_123")},
            name="My Device",
            manufacturer="My Company",
            model="Model X",
        )

    async def async_setup_sensors(self, async_add_entities: AddEntitiesCallback):
        """Set up synthetic sensors under this integration's device."""
        # Create the synthetic sensors integration
        synthetic_integration = SyntheticSensorsIntegration(self.hass)

        # Create sensor manager with device integration
        self.sensor_manager = await synthetic_integration.create_managed_sensor_manager(
            add_entities_callback=async_add_entities,
            device_info=self.device_info,
            entity_prefix="my_device",
            lifecycle_managed_externally=True,
            hass_override=self.hass,  # Parent controls HA instance
        )

        # Load and apply configuration
        yaml_config = """
        version: "1.0"
        sensors:
          power_efficiency:
            name: "Power Efficiency"
            formula: "solar_power / total_power * 100"
            variables:
              solar_power: "sensor.solar_inverter_power"
              total_power: "sensor.total_consumption"
            unit_of_measurement: "%"
        """

        config = await self.sensor_manager.load_config_from_yaml(yaml_config)
        await self.sensor_manager.apply_config(config)

    async def async_update_data(self):
        """Update integration data - synthetic sensors update automatically."""
        # Your integration's normal update logic
        # Synthetic sensors will be updated by their own coordinator
        # which is managed by this integration's lifecycle
        pass

    async def async_unload(self):
        """Unload the integration and clean up synthetic sensors."""
        if self.sensor_manager:
            await self.sensor_manager.async_unload()
```

## Exception Handling

The package follows Home Assistant's coordinator exception handling patterns. This pattern ensures proper error
classification and graceful degradation.

### Exception Hierarchy

**Base Exception Classes** (inherit from HA standard exceptions):

- `SyntheticSensorsError` - Base for all package errors
- `SyntheticSensorsConfigError` - Configuration issues (inherits from `ConfigEntryError`)
- `SyntheticSensorsNotReadyError` - Integration not ready (inherits from `ConfigEntryNotReady`)

**Specific Exception Categories**:

- **Formula Evaluation**: `FormulaSyntaxError`, `MissingDependencyError`, `UnavailableDependencyError`
- **Collection Functions**: `InvalidCollectionPatternError`, `EmptyCollectionError`
- **Sensor Management**: `SensorConfigurationError`, `SensorCreationError`, `SensorUpdateError`
- **Integration Lifecycle**: `IntegrationSetupError`, `IntegrationTeardownError`

### Error Classification

The package uses a **two-tier error handling system** following HA coordinator patterns:

**Tier 1 - Fatal Errors** (permanent configuration issues):

- Syntax errors in formulas
- Missing entities (typos in entity IDs)
- Invalid collection patterns
- Configuration schema violations
- Triggers circuit breaker to prevent repeated failures

**Tier 2 - Transitory Errors** (temporary conditions):

- Unavailable entities (network issues, device offline)
- Non-numeric states from normally numeric sensors
- Cache invalidation errors
- Allows graceful degradation with "unknown" state

### Integration with Parent Coordinators

When used within custom integrations, the exception handling integrates seamlessly:

```python
class MyCustomIntegration:
    async def async_update_data(self):
        """Update integration data with proper error handling."""
        try:
            # Your integration's update logic
            await self.update_device_data()

            # Synthetic sensors handle their own errors gracefully
            # Fatal errors are logged but don't crash the coordinator
            # Transitory errors result in "unknown" state until resolved

        except ConfigEntryNotReady as err:
            # HA will retry setup later
            raise UpdateFailed(f"Device not ready: {err}") from err
        except ConfigEntryAuthFailed as err:
            # HA will prompt for re-authentication
            raise err
        except Exception as err:
            # Temporary issues - coordinator will retry
            raise UpdateFailed(f"Update failed: {err}") from err
```

**Error State Propagation**:

- **Fatal errors** → Sensor state becomes "unavailable"
- **Transitory errors** → Sensor state becomes "unknown"
- **Successful evaluation** → Sensor state becomes "ok" (resets error counters)

This approach ensures that temporary issues (like a sensor going offline) don't
permanently break your synthetic sensors, while configuration errors are
clearly identified and prevent resource waste.

## Dependencies

Core dependencies:

- `pyyaml` - YAML configuration parsing
- `simpleeval` - Safe mathematical expression evaluation
- `voluptuous` - Configuration validation

Development dependencies:

- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `ruff` - Code linting and import sorting
- `mypy` - Type checking
- `bandit` - Security scanning
- `pre-commit` - Git hook management

## Development commands

```bash
# Install pre-commit hooks (required for all developers)
poetry run pre-commit install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/ha_synthetic_sensors

# Format code
poetry run black --line-length 88 .

# Lint code
poetry run ruff check --fix .

# Type checking
poetry run mypy src/ha_synthetic_sensors

# Run all pre-commit hooks
poetry run pre-commit run --all-files

# Fix markdown files (if markdownlint fails)
./scripts/fix-markdown.sh
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. **All developers must install them locally**:

```bash
poetry run pre-commit install
```

**Important**: The pre-commit hooks will **check** markdown files but **not automatically fix** them. If markdownlint fails, you must run the fix script locally:

```bash
./scripts/fix-markdown.sh
```

This ensures that all markdown formatting is done locally before pushing to GitHub, preventing CI failures due to file modifications.

## Architecture

Core components:

- `ConfigManager` - YAML configuration loading and validation
- `Evaluator` - Mathematical expression evaluation with caching
- `NameResolver` - Entity ID resolution and variable mapping
- `SensorManager` - Sensor lifecycle management
- `ServiceLayer` - Home Assistant service integration
- `SyntheticSensorsIntegration` - Main integration class

## License

MIT License

## Repository

- GitHub: <https://github.com/SpanPanel/ha-synthetic-sensors>
- Issues: <https://github.com/SpanPanel/ha-synthetic-sensors/issues>
