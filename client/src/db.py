from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS


def create_client(url, token, org):
    return InfluxDBClient(url=url, token=token, org=org)


def write(
        client: InfluxDBClient,
    bucket_name,
    point_name,
    tag_key_name,
    tag_value_name,
    field_name,
    value
):
    point = Point(point_name) \
        .tag(tag_key_name, tag_value_name) \
        .field(field_name, value)

    write_api = client.write_api(write_options=ASYNCHRONOUS)
    write_api.write(bucket=bucket_name, record=point)
