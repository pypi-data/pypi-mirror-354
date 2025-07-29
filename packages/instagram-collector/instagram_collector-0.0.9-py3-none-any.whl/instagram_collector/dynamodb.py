import boto3


class DynamoDB:
    def __init__(self, region_name=None):
        self.client = boto3.client("dynamodb", region_name=region_name)

    def put_item(self, table_name, item):
        return self.client.put_item(TableName=table_name, Item=item)

    def batch_write_item(self, table_name, items):
        put_requests = list(map(lambda x: {"PutRequest": {"Item": x}}, items))
        return self.client.batch_write_item(RequestItems={table_name: put_requests})

    def get_item(self, table_name, key):
        response = self.client.get_item(TableName=table_name, Key=key)

        return response.get("Item")

    def delete_item(self, table_name, key):
        return self.client.delete_item(TableName=table_name, Key=key)

    def update_item(
        self,
        table_name,
        key,
        update_expression,
        expression_attribute_values,
        expression_attribute_names={},
    ):
        if expression_attribute_names:
            return self.client.update_item(
                TableName=table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )
        else:
            return self.client.update_item(
                TableName=table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="UPDATED_NEW",
            )

    def query_with(self, table_name, key_condition_expression, expression_attribute_values, expression_attribute_names=None, filter_expression=None, index_name=None):

        additional_param = dict()
        if index_name:
            additional_param['IndexName'] = index_name
        if filter_expression:
            additional_param['FilterExpression'] = filter_expression
        if expression_attribute_names:
            additional_param['ExpressionAttributeNames'] = expression_attribute_names

        items = []
        while True:
            response = self.client.query(
                TableName=table_name,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute_values,
                **additional_param
            )

            items = items + response["Items"]

            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break
            additional_param['ExclusiveStartKey'] = last_evaluated_key

        return items

    def batch_get_item(self, table_name, keys):

        print(keys)
        response = self.client.batch_get_item(RequestItems={table_name: {"Keys": keys}})
        return response["Responses"][table_name]
