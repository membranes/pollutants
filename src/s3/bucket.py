"""
Module bucket.py
"""
import boto3
import botocore.exceptions

import src.elements.parameters as pr
import src.elements.service as sr


class Bucket:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/index.html
    """

    def __init__(self, service: sr.Service, parameters: pr.Parameters):
        """
        Constructor

        :param service: The service objects are for Amazon S3 interactions.
        :param parameters: The overarching S3 parameters settings of this project, e.g., region code
                           name, bucket name, etc.
        """

        self.__parameters: pr.Parameters = parameters
        self.__s3_resource: boto3.session.Session.resource = service.s3_resource

        # A bucket instance
        self.__bucket = self.__s3_resource.Bucket(name=self.__parameters.bucket_name)

    def create(self) -> bool:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/create.html

        :return:
        """

        if self.exists():
            return True

        create_bucket_configuration = {
            'LocationConstraint': self.__parameters.location_constraint
        }
        try:
            self.__bucket.create(ACL=self.__parameters.access_control_list,
                                 CreateBucketConfiguration=create_bucket_configuration)
            self.__bucket.wait_until_exists()
            return True or False
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

    def empty(self) -> bool:
        """
        Delete a bucket's objects

        :return:
        """

        if not self.exists():
            return True

        try:
            state = self.__bucket.objects.delete()
            return True if not state else False
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

    def delete(self) -> bool:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/objects.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/delete.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/wait_until_not_exists.html

        :return:
        """

        if not self.exists():
            return True

        # Ensure the bucket is empty.  Subsequently, delete the bucket.
        try:
            self.empty()
            self.__bucket.delete()
            self.__bucket.wait_until_not_exists()
            return True or False
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

    def exists(self) -> bool:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_bucket.html#S3.Client.head_bucket
        https://awscli.amazonaws.com/v2/documentation/api/2.0.34/reference/s3api/head-bucket.html

        :return:
        """

        try:
            state: dict = self.__bucket.meta.client.head_bucket(Bucket=self.__bucket.name)
        except botocore.exceptions.ClientError as err:
            raise Exception(err) from err

        return True if 'BucketRegion' in state.keys() else False
