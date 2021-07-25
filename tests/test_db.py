from tests.base import CligoDBTestCase


class CliDBTest(CligoDBTestCase):

    def test_check_db_config_works(self):
        from tests.utils.models import User
        self.app.db.models.register([User])

        User.create(username='user1')
        User.create(username='user2')

        users = [user for user in User.select()]

        self.assertTrue(users)
