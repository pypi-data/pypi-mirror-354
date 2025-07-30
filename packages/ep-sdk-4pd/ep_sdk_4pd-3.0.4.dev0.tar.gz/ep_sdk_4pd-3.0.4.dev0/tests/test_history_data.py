import datetime
from turtle import pd

from ep_sdk_4pd.ep_data import EpData
from ep_sdk_4pd.ep_system import EpSystem


def test_history_data():
    print('-------------test_history_data-------------')

    data = EpData.get_history_data(scope="plant",days=1)
    print(data.get("plant"))
    print('-------------------------------------')


if __name__ == '__main__':
    test_history_data()
