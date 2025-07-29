import json
import pytest
import logging
from pathlib import Path
from jsonifyer import convert_xml, convert_csv, convert_txt
from jsonifyer.config import init_directory_manager, get_directory_manager
from jsonifyer.converter.python_converter import parse_xml_to_json
import xml.etree.ElementTree as ET

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def test_env():
    base_dir = Path(__file__).parent

    dir_manager = init_directory_manager(str(base_dir))

    for dir_type in ['csv_files', 'xml_files', 'text_files']:
        input_dir = base_dir / 'input' / dir_type
        output_dir = base_dir / 'output' / dir_type
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

    for dir_type in ['csv_files', 'xml_files', 'text_files']:
        output_dir = base_dir / 'output' / dir_type
        if output_dir.exists():
            files = list(output_dir.glob('*.json'))
            if files:
                logger.info(f"\n{dir_type}:")
                for f in files:
                    logger.info(f"  - {f.name}")

    return dir_manager

def test_convert_csv_vulcanoes(test_env):
    dir_manager = test_env
    input_file = dir_manager.get_input_dir('csv') / 'vulcanoes.csv'
    output_dir = dir_manager.get_output_dir('csv')

    from jsonifyer.converter.python_converter import convert_csv
    field_map = {
        'name': 0,
        'location': 1,
        'last_eruption': 2,
        'height': 3,
        'type': 4
    }

    result = convert_csv(
        str(input_file),
        str(output_dir),
        skiprows=1,
        field_map=field_map
    )

    files = list(output_dir.glob('*.json'))
    assert len(files) > 0, f"No JSON files were created in {output_dir}"

    record_file = output_dir / 'record_1.json'
    assert record_file.exists(), f"File record_1.json was not created in {output_dir}"

    with open(record_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert isinstance(data, dict), "The JSON file must contain an object"
        assert 'name' in data, "The JSON must contain the 'name' field"
        assert 'location' in data, "The JSON must contain the 'location' field"
        assert 'last_eruption' in data, "The JSON must contain the 'last_eruption' field"

def test_convert_txt_vulcanoes(test_env):
    dir_manager = test_env
    input_file = dir_manager.get_input_dir('txt') / 'vulcanoes.txt'
    output_dir = dir_manager.get_output_dir('txt')

    result = convert_txt(
        str(input_file),
        output_path=str(output_dir),
        delimiter='~'
    )

    files = list(output_dir.glob('*.json'))
    assert len(files) > 0, f"No JSON files were created in {output_dir}"

    record_file = output_dir / 'record_1.json'
    assert record_file.exists(), f"File record_1.json was not created in {output_dir}"

    with open(record_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert isinstance(data, dict), "The JSON file must contain an object"
        assert 'name' in data, "The JSON must contain the 'name' field"
        assert 'height' in data, "The JSON must contain the 'height' field"
        assert 'type' in data, "The JSON must contain the 'type' field"

def test_convert_xml_vulcanoes_full(test_env):
    dir_manager = test_env
    input_file = dir_manager.get_input_dir('xml/volcanos')
    output_file = dir_manager.get_output_dir('xml/volcanos')

    field_map = {
        'name': './/name',
        'location.country': './/location/country',
        'location.region': './/location/region',
        'location.coordinates.latitude': './/location/coordinates/latitude',
        'location.coordinates.longitude': './/location/coordinates/longitude',
        'last_eruption.date': './/last_eruption/date',
        'last_eruption.magnitude': './/last_eruption/magnitude',
        'last_eruption.casualties': './/last_eruption/casualties',
        'height.meters': './/height/meters',
        'height.feet': './/height/feet',
        'type': './/type',
        'description.summary': './/description/summary',
        'description.history.events': ['.//description/history/event/year', './/description/history/event/description'],
        'description.geology.formation': './/description/geology/formation',
        'description.geology.composition.materials': './/description/geology/composition/material',
        'monitoring.status': './/monitoring/status',
        'monitoring.last_inspection': './/monitoring/last_inspection',
        'monitoring.risk_level': './/monitoring/risk_level',
        'monitoring.sensors': ['.//monitoring/sensors/sensor/type', './/monitoring/sensors/sensor/location', './/monitoring/sensors/sensor/status']
    }

    ET.register_namespace('v3', 'urn:hl7-org:v3')

    print(f"Input file path: {input_file}")
    print(f"Input file exists: {input_file.exists()}")

    if input_file.exists():
        tree = ET.parse(input_file)
        root = tree.getroot()
        print(f"Root tag: {root.tag}")
        print(f"Root attributes: {root.attrib}")

        for child in root:
            print(f"Child tag: {child.tag}")

    print("\nDEBUG: Test field_map:")
    print(f"field_map type: {type(field_map)}")
    print(f"field_map content: {field_map}")

    result = convert_xml(
        str(input_file),
        field_map=field_map,
        output_dir=str(output_file.parent),
        root_tag='vulcano',
        namespaces={'v3': 'urn:hl7-org:v3'}
    )

    print("\nDEBUG: Test result:")
    print(f"Result type: {type(result)}")
    print(f"Result content: {result}")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    assert output_file.exists(), f"Output file was not created in {output_file}"

    assert 'name' in result
    assert 'location' in result
    assert 'last_eruption' in result
    assert 'height' in result
    assert 'type' in result
    assert 'description' in result
    assert 'monitoring' in result

    assert 'country' in result['location']
    assert 'region' in result['location']
    assert 'coordinates' in result['location']
    assert 'date' in result['last_eruption']
    assert 'magnitude' in result['last_eruption']
    assert 'meters' in result['height']
    assert 'feet' in result['height']
    assert 'summary' in result['description']
    assert 'history' in result['description']
    assert 'geology' in result['description']
    assert 'status' in result['monitoring']
    assert 'sensors' in result['monitoring']

def test_convert_xml_vulcanoes_parts(test_env):
    dir_manager = test_env
    input_file = dir_manager.get_input_dir('xml') / 'vulcanoes.xml'
    output_file = dir_manager.get_output_dir('xml') / 'vulcanoes_parts.json'

    fields = [
        './/name',
        './/location',
        './/last_eruption',
        './/height',
        './/type'
    ]

    result = parse_xml_to_json(
        str(input_file),
        fields=fields,
        namespaces={'v3': 'urn:hl7-org:v3'},
        root_tag='vulcano'
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    assert output_file.exists(), f"Output file was not created in {output_file}"

    assert 'name' in result
    assert 'location' in result
    assert 'last_eruption' in result
    assert 'height' in result
    assert 'type' in result

def test_convert_xml_vulcanoes_auto(test_env):
    dir_manager = test_env
    input_dir = dir_manager.get_input_dir('xml') / "volcanos"
    output_dir = dir_manager.get_output_dir('xml') / "volcanos"

    # Convert the entire XML file without specifying fields
    result = convert_xml(
        str(input_dir),
        "blah.bloah",
        "name",
        str(output_dir),
        converter="python",
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'vulcanoes_auto.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    assert output_file.exists(), f"Output file was not created at {output_file}"

    # Check if the result contains the expected basic structure
    assert isinstance(result, dict), "The result must be a dictionary"
    assert len(result) > 0, "The result must not be empty"

    # Check if it contains the main tags of the document
    assert 'name' in result, "The result must contain the volcano name"
    assert 'location' in result, "The result must contain the location"
    assert 'last_eruption' in result, "The result must contain the last eruption"
    assert 'height' in result, "The result must contain the height"
    assert 'type' in result, "The result must contain the type"
    assert 'description' in result, "The result must contain the description"
    assert 'monitoring' in result, "The result must contain monitoring information"

    # Check the structure of the location
    assert 'country' in result['location'], "The location must contain the country"
    assert 'region' in result['location'], "The location must contain the region"
    assert 'coordinates' in result['location'], "The location must contain the coordinates"
    assert 'latitude' in result['location']['coordinates'], "The coordinates must contain the latitude"
    assert 'longitude' in result['location']['coordinates'], "The coordinates must contain the longitude"

    # Check the structure of the last eruption
    assert 'date' in result['last_eruption'], "The last eruption must contain the date"
    assert 'magnitude' in result['last_eruption'], "The last eruption must contain the magnitude"
    assert 'casualties' in result['last_eruption'], "The last eruption must contain the number of casualties"

    # Check the structure of the height
    assert 'meters' in result['height'], "The height must contain meters"
    assert 'feet' in result['height'], "The height must contain feet"

    # Check the structure of the description
    assert 'summary' in result['description'], "The description must contain a summary"
    assert 'history' in result['description'], "The description must contain the history"
    assert 'geology' in result['description'], "The description must contain geological information"

    # Check the structure of the monitoring
    assert 'status' in result['monitoring'], "The monitoring must contain the status"
    assert 'last_inspection' in result['monitoring'], "The monitoring must contain the last inspection"
    assert 'risk_level' in result['monitoring'], "The monitoring must contain the risk level"
    assert 'sensors' in result['monitoring'], "The monitoring must contain the sensors"

    print("Automatic XML conversion test completed successfully!")
    print(f"Result saved at: {output_file}")
