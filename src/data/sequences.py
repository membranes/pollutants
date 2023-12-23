import src.functions.objects
import logging
import pandas as pd


class Sequences:

    def __init__(self):
        """

        """

        self.__url = 'https://www.scottishairquality.scot/sos-scotland/api/v1/timeseries'

        labels = ['id', 'label', 'uom', 'station.properties.id', 'station.properties.label']
        names = ['sequence_id', 'description', 'unit_of_measure', 'station_id', 'station_label']
        self.__rename = dict(zip(labels, names))

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def __structure(blob: dict) -> pd.DataFrame:

        try:
            normalised = pd.json_normalize(data=blob, max_level=2)
        except ImportError as err:
            raise Exception(err) from err

        coordinates = pd.DataFrame(data=normalised['station.geometry.coordinates'].to_list(),
                                   columns=['longitude', 'latitude', 'height'])
        data = normalised.copy().drop(columns='station.geometry.coordinates').join(coordinates, how='left')
        data.drop(columns=['station.type', 'station.geometry.type', 'height'], inplace=True)

        return data

    @staticmethod
    def __feature_engineering(blob: pd.DataFrame) -> pd.DataFrame:

        data = blob.copy()

        identifiers: pd.DataFrame = data.copy()['description'].str.split(n=1, expand=True)
        identifiers = identifiers.copy().loc[:, 0].str.rsplit(pat='/', n=1, expand=True)
        data.loc[:, 'pollution_id'] = identifiers.loc[:, 1].astype(dtype=int).array
        data.drop(columns='description', inplace=True)

        return data

    def exc(self):

        objects = src.functions.objects.Objects()
        dictionary = objects.api(url=self.__url)

        data = self.__structure(blob=dictionary)
        data.rename(columns=self.__rename, inplace=True)
        data = self.__feature_engineering(blob=data)
        self.__logger.info(data.info())
        self.__logger.info(data.head())
