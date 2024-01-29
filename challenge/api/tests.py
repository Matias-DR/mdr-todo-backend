from rest_framework.test import APITestCase


def PRINT(
    msg: str,
    result: any
):
    if hasattr(result, 'data'):
        data = result.data
    else:
        data = 'NO .DATA'
    code = result.status_code
    print(f'{msg} -> {data, code}')


class UserViewTestCase(APITestCase):
    def setUp(self):
        self.forms = {
            'with_full_data': {
                'username': 'test',
                'password': 'test'
            },
            'with_full_data2': {
                'username': 'test2',
                'password': 'test2'
            },
            'without_username': {
                'password': 'test'
            },
            'without_password': {
                'username': 'test'
            },
            'wrong_password': {
                'username': 'test',
                'password': 'wrong'
            },
            'wrong_username': {
                'username': 'wrong',
                'password': 'test'
            },
            'empty_form': {}
        }
        # Create a user
        self.client.post(
            '/api/user/',
            self.forms['with_full_data'],
            format='json'
        )

    def test_signup(self):
        def response(form: str):
            return self.client.post(
                '/api/user/',
                self.forms[form],
                format='json'
            )

        def ok():
            result = response('with_full_data2')
            PRINT(
                'UserViewTestCase test_signup ok',
                result
            )
            self.assertEqual(result.status_code, 201)

        def without_username():
            result = response('without_username')
            PRINT(
                'UserViewTestCase test_signup without_username',
                result
            )
            self.assertEqual(result.status_code, 400)

        def without_password():
            result = response('without_password')
            PRINT(
                'UserViewTestCase test_signup without_password',
                result
            )
            self.assertEqual(result.status_code, 400)

        def empty_form():
            result = response('empty_form')
            PRINT(
                'UserViewTestCase test_signup empty_form',
                result
            )
            self.assertEqual(result.status_code, 400)

        ok()
        without_username()
        without_password()
        empty_form()

    def test_signin(self):
        def response(user_type: str):
            return self.client.post(
                '/api/token/',
                self.forms[user_type],
                format='json'
            )

        def ok():
            result = response('with_full_data')
            PRINT(
                'UserViewTestCase test_signin ok',
                result
            )
            self.assertEqual(result.status_code, 200)

        def without_username():
            result = response('without_username')
            PRINT(
                'UserViewTestCase test_signin without_username',
                result
            )
            self.assertEqual(result.status_code, 400)

        def without_password():
            result = response('without_password')
            PRINT(
                'UserViewTestCase test_signin without_password',
                result
            )
            self.assertEqual(result.status_code, 400)

        def wrong_password():
            result = response('wrong_password')
            PRINT(
                'UserViewTestCase test_signin wrong_password',
                result
            )
            self.assertEqual(result.status_code, 401)

        def wrong_username():
            result = response('wrong_username')
            PRINT(
                'UserViewTestCase test_signin wrong_username',
                result
            )
            self.assertEqual(result.status_code, 401)

        def empty_form():
            result = response('empty_form')
            PRINT(
                'UserViewTestCase test_signin empty_form',
                result
            )
            self.assertEqual(result.status_code, 400)

        ok()
        without_username()
        without_password()
        wrong_password()
        wrong_username()
        empty_form()


class TaskViewTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.client.post(
            '/api/user/',
            {
                'username': 'test',
                'password': 'test'
            },
            format='json'
        )
        # Sign in with the user
        signin_result = self.client.post(
            '/api/token/',
            {
                'username': 'test',
                'password': 'test'
            },
            format='json'
        )
        # Save the token
        self.token = signin_result.data['access']

    def test_post(self):
        forms = {
            'with_full_data': {
                'title': 'test3',
                'description': 'test3'
            },
            'without_title': {
                'description': 'test3'
            },
            'without_description': {
                'title': 'test3'
            },
            'empty_form': {}
        }

        def response(
            form: str,
            auth: bool = True
        ):
            return self.client.post(
                '/api/task/',
                forms[form],
                format='json',
                HTTP_AUTHORIZATION=f'Bearer {self.token}' if auth else None
            )

        def ok():
            result = response('with_full_data')
            PRINT(
                'TaskViewTestCase test_post ok',
                result
            )
            self.assertEqual(result.status_code, 201)

        def without_title():
            result = response('without_title')
            PRINT(
                'TaskViewTestCase test_post without_title',
                result
            )
            self.assertEqual(result.status_code, 400)

        def without_description():
            result = response('without_description')
            PRINT(
                'TaskViewTestCase test_post without_description',
                result
            )
            self.assertEqual(result.status_code, 400)

        def empty_form():
            result = response('empty_form')
            PRINT(
                'TaskViewTestCase test_post empty_form',
                result
            )
            self.assertEqual(result.status_code, 400)

        def unauthorized():
            result = response('with_full_data', False)
            PRINT(
                'TaskViewTestCase test_post unauthorized',
                result
            )
            self.assertEqual(result.status_code, 401)

        ok()
        without_title()
        without_description()
        empty_form()
        unauthorized()

    def test_complete(self):
        # Create the task
        self.client.post(
            '/api/task/',
            {
                'title': 'test1',
                'description': 'test1'
            },
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        def response(
            pk: int = 1,
            auth: bool = True
        ):
            return self.client.put(
                f'/api/task/{pk}/complete/',
                format='json',
                HTTP_AUTHORIZATION=f'Bearer {self.token}' if auth else None
            )

        def complete_an_uncompleted_task():
            result = response()
            PRINT(
                'TaskViewTestCase test_complete complete_an_uncompleted_task',
                result
            )
            self.assertEqual(result.status_code, 200)

        def complete_a_completed_task():
            result = response()
            PRINT(
                'TaskViewTestCase test_complete complete_a_completed_task',
                result
            )
            self.assertEqual(result.status_code, 200)

        def unauthorized():
            result = response(auth=False)
            PRINT(
                'TaskViewTestCase test_complete unauthorized',
                result
            )
            self.assertEqual(result.status_code, 401)

        def not_exists():
            result = response(pk=0)
            PRINT(
                'TaskViewTestCase test_complete not_exists',
                result
            )
            self.assertEqual(result.status_code, 404)

        complete_an_uncompleted_task()
        complete_a_completed_task()
        unauthorized()
        not_exists()

    def test_incomplete(self):
        # Create the task
        self.client.post(
            '/api/task/',
            {
                'title': 'test1',
                'description': 'test1'
            },
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        # Complete the task
        self.client.put(
            '/api/task/1/complete/',
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        def response(
            pk: int = 1,
            auth: bool = True
        ):
            return self.client.put(
                f'/api/task/{pk}/incomplete/',
                format='json',
                HTTP_AUTHORIZATION=f'Bearer {self.token}' if auth else None
            )

        def incomplete_a_completed_task():
            result = response()
            PRINT(
                'TaskViewTestCase test_incomplete incomplete_a_completed_task',
                result
            )
            self.assertEqual(result.status_code, 200)

        def incomplete_an_uncompleted_task():
            result = response()
            PRINT(
                'TaskViewTestCase test_incomplete incomplete_an_uncompleted_task',
                result
            )
            self.assertEqual(result.status_code, 200)

        def unauthorized():
            result = response(auth=False)
            PRINT(
                'TaskViewTestCase test_incomplete unauthorized',
                result
            )
            self.assertEqual(result.status_code, 401)

        def not_exists():
            result = response(pk=0)
            PRINT(
                'TaskViewTestCase test_incomplete not_exists',
                result
            )
            self.assertEqual(result.status_code, 404)

        incomplete_a_completed_task()
        incomplete_an_uncompleted_task()
        unauthorized()
        not_exists()

    def test_get(self):
        # Create the first task
        self.client.post(
            '/api/task/',
            {
                'title': 'test1',
                'description': 'test1'
            },
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        # Create the second task
        self.client.post(
            '/api/task/',
            {
                'title': 'test2',
                'description': 'test2'
            },
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        # Complete the second task
        self.client.put(
            '/api/task/2/complete/',
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        def response(
            pk: int | None = None,
            auth: bool = True,
            search: str | None = None,
            filter: str | None = None,
            print_url: bool = False
        ):
            url = f'/api/task{
                '/' if search is None and filter is None else '?'
            }{
                f'{pk}/' if pk is not None else ''
            }{
                f'search={search}' if search else ''
            }{
                f'{filter}' if filter is not None else ''
            }'
            if print_url:
                print(url)
            return self.client.get(
                url,
                format='json',
                HTTP_AUTHORIZATION=f'Bearer {self.token}' if auth else None
            )

        def one():
            result = response(pk=1)
            PRINT(
                'TaskViewTestCase test_get one',
                result
            )
            self.assertEqual(result.status_code, 200)

        def all():
            result = response()
            PRINT(
                'TaskViewTestCase test_get all',
                result
            )
            self.assertEqual(result.status_code, 200)

        def search_found():
            result = response(search='test', print_url=True)
            PRINT(
                'TaskViewTestCase test_get search_found',
                result
            )
            self.assertEqual(result.status_code, 200)

        def search_not_found():
            result = response(search='not_found')
            PRINT(
                'TaskViewTestCase test_get search_not_found',
                result
            )
            self.assertEqual(result.status_code, 200)

        def filter_found():
            result = response(filter='completed=true')
            PRINT(
                'TaskViewTestCase test_get filter_found',
                result
            )
            self.assertEqual(result.status_code, 200)

        def filter_not_found():
            result = response(filter='completed=false')
            PRINT(
                'TaskViewTestCase test_get filter_not_found',
                result
            )
            self.assertEqual(result.status_code, 200)

        def unauthorized():
            result = response(auth=False)
            PRINT(
                'TaskViewTestCase test_get unauthorized',
                result
            )
            self.assertEqual(result.status_code, 401)

        def not_exists():
            result = response(pk=0)
            PRINT(
                'TaskViewTestCase test_get not_exists',
                result
            )
            self.assertEqual(result.status_code, 404)

        one()
        all()
        search_found()
        search_not_found()
        filter_found()
        filter_not_found()
        unauthorized()
        not_exists()
