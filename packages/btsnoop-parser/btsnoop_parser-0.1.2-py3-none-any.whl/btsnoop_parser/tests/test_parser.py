from btsnoop_parser.core import parse_btsnoop_file
from btsnoop_parser.hci_decoder import decode_hci_packet
import os

def test_can_parse_sample_file():
    sample_file = os.path.join(os.path.dirname(__file__), "sample.btsnoop")
    records = parse_btsnoop_file(sample_file)
    assert isinstance(records, list)
    assert len(records) > 0

def test_record_has_expected_fields():
    sample_file = os.path.join(os.path.dirname(__file__), "sample.btsnoop")
    records = parse_btsnoop_file(sample_file)
    record = records[0]
    assert 'timestamp' in record
    assert 'direction' in record
    assert record['direction'] in ('TX', 'RX')
    assert 'packet_data' in record

def test_can_decode_command():
    sample_file = os.path.join(os.path.dirname(__file__), "sample.btsnoop")
    records = parse_btsnoop_file(sample_file)
    command_record = next(r for r in records if r['packet_type'] == 0x01)
    decoded = decode_hci_packet("COMMAND", command_record['packet_data'])
    assert decoded['type'] == "COMMAND"
    assert 'opcode' in decoded
    assert 'name' in decoded
