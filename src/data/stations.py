"""Module stations.py"""
import logging

import src.functions.objects

class Stations:
    """
    Class Stations
    Reads-in the Scottish Air Quality Agency's inventory of telemetric devices
    """

    def __init__(self):
        """
        Constructor
        """

        self.__url = 'https://www.scottishairquality.scot/sos-scotland/api/v1/stations'

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        data: dict = objects.api(url=self.__url)
        self.__logger.info(data)