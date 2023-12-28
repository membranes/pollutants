"""
Module upload.py
"""
import io

import boto3
import botocore.exceptions
import pandas as pd

import src.elements.parameters
import src.elements.service


class Upload:
    """
    Cf. the Action sections of
          * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/index.html
          * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/object/index.html#S3.Object

        The second is derivable from the first via
          * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/Object.html
    """

    def __init__(self, service: src.elements.service.Service):
        """

        :param service:
        """

        self.__parameters: src.elements.parameters.Parameters = service.parameters
        self.__s3_resource: boto3.session.Session.resource = service.s3_resource

    def bytes(self, data: pd.DataFrame, metadata: dict, key_name: str) -> bool:
        """

        :param data: The data that will be delivered to Amazon S3
        :param metadata: The metadata of the data
        :param key_name: The key name of the data -> {}/{}/{}.csv
        :return:
        """

        buffer = io.StringIO()
        data.to_csv(path_or_buf=buffer, header=True, index=False, encoding='utf-8')

        # A bucket object
        bucket = self.__s3_resource.Bucket(name=self.__parameters.bucket_name)

        try:
            bucket.put_object(
                ACL=self.__parameters.access_control_list,
                Body=buffer.getvalue(),
                Key=key_name, Metadata=metadata)
            return True or False
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err
