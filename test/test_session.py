import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

import session
from user import User
from booking import Booking
from space import Space

@pytest.fixture
def curr_user():
    user = User(userId=123, isLibrarian=False)
    return user

@pytest.fixture
def session_object(curr_user):
    mock_data_bookings = MagicMock(side_effect = {
        0: Booking(0, 2, "cdong49@uwo.ca", datetime.strptime("2022-11-21 14:00",'%Y-%m-%d %H:%M'), datetime.strptime("2022-11-21 15:00",'%Y-%m-%d %H:%M')),
        1: Booking(1, 0, "eliu72@uwo.ca", datetime.strptime("2022-11-21 14:00",'%Y-%m-%d %H:%M'), datetime.strptime("2022-11-21 15:00",'%Y-%m-%d %H:%M'))
    })
    patch_loadBookings = patch("session.Session.loadBookings", mock_data_bookings)

    mock_data_spaces = MagicMock(side_effect = {
        0: Space(0, 4, {"outlets": True,"accessible": True,"quiet": False,"private": True,"media": True}, "Taylor - Room 155"),
        1: Space(1, 1, {"outlets": True,"accessible": True,"quiet": False,"private": True,"media": True}, "Taylor - Room 55")
    })
    patch_loadSpaces = patch("session.Session.loadSpaces", mock_data_spaces)

    with patch_loadBookings as p1:
        with patch_loadSpaces as p2:
            return session.Session(curr_user)


def test_loadBookings(session_object):
    # patch open since we don't want to actually open the file
    patch_open = patch("builtins.open", MagicMock())

    # provide mock data for tests
    mock_data = MagicMock(side_effect = [ 
        {
            "bookingId": 0,
            "spaceId": 2,
            "userEmail": "cdong49@uwo.ca",
            "startTime": "2022-11-21 14:00",
            "endTime": "2022-11-21 16:00"
        },
        {
            "bookingId": 1,
            "spaceId": 0,
            "userEmail": "eliu72@uwo.ca",
            "startTime": "2022-11-21 11:00",
            "endTime": "2022-11-21 13:00"
        }])
    patch_json_load = patch("json.load", mock_data)

    # with patch_open as p_open:
    #     with patch_json_load as p_json_load:
            
    assert type(session_object == session.Session)
            
