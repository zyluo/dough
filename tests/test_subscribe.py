import unittest
import mox


class UnknownPersonError(Exception):
    pass


class PersonDao(object):

    def InsertPerson(self, func):
        return 1

    def UpdatePerson(self, func):
        pass

    def DeletePerson(self, func):
        pass


class SubscribeTest(unittest.TestCase):

    def setUp(self):
        # Create an instance of Mox
        self.person_mocker = mox.Mox()

    def tearDown(self):
        self.person_mocker.UnsetStubs()

    def testUsingMox(self):
        # Create a mock PersonDao
        dao = self.person_mocker.CreateMock(PersonDao)

        test_person = dict()
        test_primary_key = 1
        unknown_person = dict()
        # Return a value when this method is called
        dao.InsertPerson(test_person).AndReturn(test_primary_key)

        # Void method
        dao.UpdatePerson(test_person)

        # Raise an exception when this is called
        dao.DeletePerson(unknown_person).\
                AndRaise(UnknownPersonError('id not found'))

        # Put all mocks created by mox into replay mode
        self.person_mocker.ReplayAll()

        # Run the test
        ret_pk = dao.InsertPerson(test_person)
        dao.UpdatePerson(test_person)
        self.assertRaises(UnknownPersonError, dao.DeletePerson, unknown_person)

        # Verify all mocks were used as expected, and tests ran properly
        self.person_mocker.VerifyAll()
        self.assertEquals(test_primary_key, ret_pk)
