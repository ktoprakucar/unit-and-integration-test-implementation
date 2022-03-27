import pandas as pd

from src.model.musician import Musician


class Mapper:

    @staticmethod
    def convert_dataframe_to_musician(musician_df: pd.Series) -> Musician:
        return Musician(name=musician_df['name'],
                        surname=musician_df['surname'],
                        age=musician_df['age'],
                        instrument=musician_df['instrument'])

    @classmethod
    def convert_musician_to_dataframe(cls, musician: Musician) -> pd.DataFrame:
        return pd.DataFrame({'name': [musician.name],
                             'surname': [musician.surname],
                             'age': [musician.age],
                             'instrument': [musician.instrument]})
