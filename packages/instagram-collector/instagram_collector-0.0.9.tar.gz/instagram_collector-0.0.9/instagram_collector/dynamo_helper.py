import typing
from datetime import datetime
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


class CustomSerializer(TypeSerializer):
    """
    Thin wrapper around the original TypeSerializer that teaches it to:
    - Serialize datetime objects as ISO8601 strings and stores them as binary info.
    - Serialize float objects as strings and stores them as binary info.
    - Deal with the above as part of sets
    """

    def _serialize_datetime(self, value) -> typing.Dict[str, bytes]:
        return {"B": f"DT:{value.isoformat(timespec='microseconds')}".encode("utf-8")}

    def _serialize_float(self, value) -> typing.Dict[str, bytes]:
        return {"B": f"FL:{str(value)}".encode("utf-8")}

    def serialize(self, value) -> typing.Dict[str, typing.Any]:
        try:
            return super().serialize(value)
        except TypeError as err:

            if isinstance(value, datetime):
                return self._serialize_datetime(value)

            if isinstance(value, float):
                return self._serialize_float(value)

            if isinstance(value, set):
                return {
                    "BS": [
                        self.serialize(v)["B"]  # Extract the bytes
                        for v in value
                    ]
                }

            # A type that the reference implementation and we
            # can't handle
            raise err


class CustomDeserializer(TypeDeserializer):
    """
    Thin wrapper around the original TypeDeserializer that teaches it to:
    - Deserialize datetime objects from specially encoded binary data.
    - Deserialize float objects from specially encoded binary data.
    """

    def _deserialize_b(self, value: bytes):
        """
        Overwrites the private method to deserialize binary information.
        """
        if value[:3].decode("utf-8") == "DT:":
            return datetime.fromisoformat(value.decode("utf-8").replace("DT:", ""))
        if value[:3].decode("utf-8") == "FL:":
            return float(value.decode("utf-8").replace("FL:", ""))

        return super()._deserialize_b(value)

    def _deserialize_n(self, value: bytes):
        """
        Overwrites the private method to deserialize decimal information.
        """
        value = super()._deserialize_n(value)
        if value % 1 == 0:
            return int(value)
        else:
            return float(value)


deserializer = CustomDeserializer()
serializer = CustomSerializer()


class DynamoHelper:
    @staticmethod
    def deserialize(document: object) -> str:
        return {k: deserializer.deserialize(v) for k, v in document.items()}

    @staticmethod
    def serialize(document: object):
        return {k: serializer.serialize(v) for k, v in document.items()}

    @staticmethod
    def serialize_in(document: object):
        return {k: {"AttributeValue": serializer.serialize(v), "ComparisonOperator": "IN"} for k, v in document.items()}

    @staticmethod
    def get_update_params(body, append_fields=[]):
        update_expression = ["SET "]
        update_values = dict()
        update_names = dict()

        for key, val in body.items():
            update_values[f":{key.replace('-', '')}"] = val

            if '-' in key:
                update_names[f"#{key.replace('-', '')}"] = key
                update_values[f":{key.replace('-', '')}"] = val
                update_expression.append(f" #{key.replace('-', '')} = :{key.replace('-', '')},")
            elif key in append_fields:
                update_names[f"#{key}"] = key
                update_values[f":{key}"] = val
                update_expression.append(f" #{key} = list_append(#{key},:{key}),")
            else:
                update_names[f"#{key}"] = key
                update_values[f":{key}"] = val
                update_expression.append(f" #{key} = :{key},")
        return "".join(update_expression)[:-1], update_values, update_names

    @staticmethod
    def get_query_params(key_data, filter_data={}, begin_with_fields=[], in_fields=[], append_fields=[], between_fields=[]):
        key_condition_expression = []
        filter_expression = []
        attribute_values = dict()
        attribute_names = dict()

        for key, val in key_data.items():
            # process for in operation
            attribute_names[f"#{key.replace('-', '')}"] = key
            if key in in_fields:
                in_expression = []
                sub_items = list(val.values())[0]
                for val_index, val_item in enumerate(sub_items):
                    # attribute_names[f"#{key.replace('-', '')}_{val_index}"] = val_item
                    attribute_values[f":{key.replace('-', '')}_{val_index}"] = val_item
                    in_expression.append(f":{key.replace('-', '')}_{val_index}")
                in_expression = ",".join(in_expression)
                key_condition_expression.append(f"#{key} in ({in_expression})")
            else:
                attribute_values[f":{key.replace('-', '')}"] = val
                if key in append_fields:
                    key_condition_expression.append(f"#{key} = list_append(#{key},:{key})")
                elif key in begin_with_fields:
                    key_condition_expression.append(f"begins_with(#{key.replace('-', '')}, :{key.replace('-', '')})")
                else:
                    key_condition_expression.append(f"#{key.replace('-', '')} = :{key.replace('-', '')}")

        if filter_data:
            for key, val in filter_data.items():
                # process for in operation
                attribute_names[f"#{key.replace('-', '')}"] = key
                if key in in_fields:
                    in_expression = []
                    sub_items = list(val.values())[0]
                    for val_index, val_item in enumerate(sub_items):
                        attribute_values[f":{key.replace('-', '')}_{val_index}"] = val_item
                        in_expression.append(f":{key.replace('-', '')}_{val_index}")
                    in_expression = ",".join(in_expression)
                    filter_expression.append(f"#{key} in ({in_expression})")
                elif key in between_fields:
                    key_low = f"{key}_low"
                    key_high = f"{key}_high"
                    print(val)
                    attribute_values[f":{key_low}"] = list(val.values())[0][0]
                    attribute_values[f":{key_high}"] = list(val.values())[0][1]
                    filter_expression.append(f"#{key} > :{key_low}")
                    filter_expression.append(f"#{key} < :{key_high}")
                else:
                    attribute_values[f":{key.replace('-', '')}"] = val
                    if key in append_fields:
                        filter_expression.append(f"#{key} = list_append(#{key},:{key})")
                    elif key in begin_with_fields:
                        filter_expression.append(f"begins_with(#{key}, :{key})")
                    else:
                        filter_expression.append(f"#{key} = :{key}")
            return " AND ".join(key_condition_expression), " AND ".join(filter_expression), attribute_values, attribute_names
        else:
            return " AND ".join(key_condition_expression), attribute_values, attribute_names
