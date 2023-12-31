"""Module parameters.py"""
import os
import yaml

import src.elements.parameters


class Parameters:
    """
    Class Parameters

    S3 Express One Zone, which has 4 overarching regions
    https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-Regions-and-Zones.html
    """

    def __init__(self):
        """
        Constructor
        """

        self.__uri = os.path.join(os.getcwd(), 'resources', 'parameters.yaml')

    def __get_dictionary(self) -> dict:

        with open(file=self.__uri, mode='r') as stream:
            try:
                blob = yaml.load(stream=stream, Loader=yaml.CLoader)
            except yaml.YAMLError as err:
                raise Exception(err) from err

        return blob['parameters']

    @staticmethod
    def __build_collection(dictionary: dict) -> src.elements.parameters.Parameters:
        """

        :param dictionary:
        :return:
        """

        parameters = src.elements.parameters.Parameters(**dictionary)

        # Parsing variables
        location_constraint = parameters.location_constraint.format(region_name=parameters.region_name)
        parameters = parameters._replace(location_constraint=location_constraint)

        return parameters

    def exc(self) -> src.elements.parameters.Parameters:
        """

        :return:
        """

        dictionary = self.__get_dictionary()

        return self.__build_collection(dictionary=dictionary)
