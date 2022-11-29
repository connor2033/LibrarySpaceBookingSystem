import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from datetime import timedelta

import session
from models.user import User
from models.booking import Booking
from models.space import Space

# Returns a test user
@pytest.fixture
def curr_user():
    user = User(userId=123, isLibrarian=False, firstName="first name", lastName="last name")
    return user

# Returns a test session object
@pytest.fixture
def session_object(curr_user):
    # mock bookings dictionary in Session object
    mock_data_bookings = MagicMock(return_value = {
        0: Booking(0, 2, "cdong49@uwo.ca", datetime.strptime("2022-11-21 14:00:00",'%Y-%m-%d %H:%M:%S'), datetime.strptime("2022-11-21 16:00:00",'%Y-%m-%d %H:%M:%S')),
        1: Booking(1, 0, "eliu72@uwo.ca", datetime.strptime("2022-11-21 11:00:00",'%Y-%m-%d %H:%M:%S'), datetime.strptime("2022-11-21 13:00:00",'%Y-%m-%d %H:%M:%S'))
    })
    patch_loadBookings = patch("session.Session.loadBookings", mock_data_bookings)

    # mock spaces dictionary in Session object
    mock_data_spaces = MagicMock(return_value = {
        0: Space(0, 4, {"outlets": True,"accessible": True,"quiet": False,"private": True,"media": True}, "Taylor - Room 155"),
        1: Space(1, 1, {"outlets": True,"accessible": True,"quiet": False,"private": True,"media": True}, "Taylor - Room 55")
    })
    patch_loadSpaces = patch("session.Session.loadSpaces", mock_data_spaces)

    # return a session object 
    with patch_loadBookings as p1:
        with patch_loadSpaces as p2:
            return session.Session(curr_user)


# test loadBookings function to check that it correctly parses the json data
def test_loadBookings(session_object):
    # patch open since we don't want to actually open the file
    patch_open = patch("builtins.open", MagicMock())

    # bookings are made for future dates since load bookings removes past bookings
    mock_data = MagicMock(return_value = [ 
        {
            "bookingId": 0,
            "spaceId": 2,
            "userEmail": "cdong49@uwo.ca",
            "startTime": "2100-11-21 14:00:00",
            "endTime": "2100-11-21 16:00:00"
        },
        {
            "bookingId": 1,
            "spaceId": 0,
            "userEmail": "eliu72@uwo.ca",
            "startTime": "2100-11-21 11:00:00",
            "endTime": "2100-11-21 13:00:00"
        }])
    patch_json_load = patch("json.load", mock_data)

    # the expected return value after parsing the json data
    expected_data = {
        0: Booking(0, 2, "cdong49@uwo.ca", datetime.strptime("2100-11-21 14:00:00",'%Y-%m-%d %H:%M:%S'), datetime.strptime("2100-11-21 16:00:00",'%Y-%m-%d %H:%M:%S')),
        1: Booking(1, 0, "eliu72@uwo.ca", datetime.strptime("2100-11-21 11:00:00",'%Y-%m-%d %H:%M:%S'), datetime.strptime("2100-11-21 13:00:00",'%Y-%m-%d %H:%M:%S'))
    }

    # using the mocks, test loadBookings function
    with patch_open as p_open:
        with patch_json_load as p_json_load:
            loaded_bookings = session_object.loadBookings()
            # check that the actual and expected have the same num of bookings
            assert len(loaded_bookings) == len(expected_data)
            # check that their values are the same
            for key in loaded_bookings.keys():
                assert loaded_bookings[key].userId == expected_data[key].userId
                assert loaded_bookings[key].start == expected_data[key].start
                assert loaded_bookings[key].end == expected_data[key].end
                assert loaded_bookings[key].spaceId == expected_data[key].spaceId


# # test loadSpaces function to check that it correctly parses the json data
def test_loadSpaces(session_object):
    # patch open since we don't want to actually open the file
    patch_open = patch("builtins.open", MagicMock())

    # provide mock data for tests
    mock_data = MagicMock(return_value = [ 
        {
            "spaceId": 0,
            "location": "Taylor - Room 155",
            "seats": 4,
            "filters": {
                "outlets": True,
                "accessible": True,
                "quiet": False,
                "private": True,
                "media": True
            }
        },
        {
            "spaceId": 1,
            "location": "Taylor - Floor G",
            "seats": 1,
            "filters": {
                "outlets": True,
                "accessible": True,
                "quiet": True,
                "private": False,
                "media": False
            }
        }])
    patch_json_load = patch("json.load", mock_data)

    # the expected return value after parsing the json data
    expected_data = {
        0: Space(0, 4, {"outlets": True,"accessible": True,"quiet": False,"private": True,"media": True}, "Taylor - Room 155"),
        1: Space(1, 1, {"outlets": True,"accessible": True,"quiet": True,"private": False,"media": False}, "Taylor - Floor G")
    }

    # using the mocks, test loadBookings function
    with patch_open as p_open:
        with patch_json_load as p_json_load:
            loaded_spaces = session_object.loadSpaces()
            # check that the actual and expected have the same num of bookings
            assert len(loaded_spaces) == len(expected_data)
            # check that their values are the same
            for key in loaded_spaces.keys():
                assert loaded_spaces[key].filters == expected_data[key].filters
                assert loaded_spaces[key].location == expected_data[key].location
                assert loaded_spaces[key].seats == expected_data[key].seats


# test add booking function to make sure that we update the dict and json data
def test_addBooking(session_object):
    # we don't want to actually write to the file so we mock this funciton
    patch_open = patch("builtins.open", MagicMock()) 
    with patch_open as p_open:
        newBooking = session_object.addBooking("12", '2022-11-28 09:00:00', '2022-11-28 10:00:00')

        # check that new booking is in the bookings dict
        assert newBooking == session_object.allBookings[newBooking.bookingId]

        # check that we tried to add to database
        p_open.assert_called_once()


# test cancelBooking function to make sure that we update the dict and json data
def test_cancelBooking(session_object):
    # we don't want to actually write to the file so we mock this funciton
    patch_open = patch("builtins.open", MagicMock())
    with patch_open as p_open:
        # add a fake booking and try to remove it
        newBooking = session_object.addBooking("13", '2022-11-28 11:00:00', '2022-11-28 12:00:00')
        newBookingId = newBooking.bookingId
        
        # remove the new booking
        session_object.cancelBooking(newBookingId)

        # check that the booking is no longer in the dict
        assert newBookingId not in session_object.allBookings

        # check that changes are saved to db
        assert p_open.call_count == 2 # 1 call for addBooking, 1 call for removeBooking


# function to make sure that adding a space updates in memory dict and database
def test_addSpace(session_object):
    # we don't want to actually write to the file so we mock this funciton
    patch_open = patch("builtins.open", MagicMock()) 
    with patch_open as p_open:
        newSpace = session_object.addSpace("Fake location", 10)

        # check that new space is in the spaces dict
        assert newSpace == session_object.allSpaces[newSpace.spaceId]
        
        # check that we tried to add to database
        p_open.assert_called_once()


# function to make sure that removing a space updates in memory dict and database
def test_removeSpace(session_object):
    # we don't want to actually write to the file so we mock this funciton
    patch_open = patch("builtins.open", MagicMock())
    patch_cancelBooking = patch("session.Session.cancelBooking")
    with patch_open as p_open:
        with patch_cancelBooking:
            # remove a space
            spaceId = 0
            session_object.removeSpace(spaceId)

            # check that the space is no longer in the dict
            assert spaceId not in session_object.allSpaces

            # check that changes are saved to db
            p_open.assert_called_once()