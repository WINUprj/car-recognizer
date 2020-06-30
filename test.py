from __future__ import unicode_literals, absolute_import

import unittest

from linebot.exceptions import LineBotApiError
from linebot.models import Error, ErrorDetail


class TestExceptions(unittest.TestCase):
    maxDiff = None

    def test_str(self):
        headers = {'X-Line-Request-Id': 'f70dd685-499a-4231-a441-f24b8d4fba21'}
        line_bot_api_error = LineBotApiError(
            status_code=400,
            request_id='f70dd685-499a-4231-a441-f24b8d4fba21',
            headers=headers,
            error=Error(message='The request body has 1 error(s)',
                        details=[ErrorDetail(message='May not be empty',
                                             property='messages[0].text')]))
        self.assertEqual(
            line_bot_api_error.__str__(),
            'LineBotApiError: status_code=400, request_id=f70dd685-499a-4231-a441-f24b8d4fba21, '
            'error_response={"details": [{"message": "May not be empty", '
            '"property": "messages[0].text"}], "message": "The request body has 1 error(s)"}, '
            + 'headers={}'.format(headers)
        )

    # def test_accepted_str(self):
    #     headers = {
    #         'X-Line-Request-Id': '123e4567-e89b-12d3-a456-426655440002',
    #         'X-Line-Accepted-Request-Id': '123e4567-e89b-12d3-a456-426655440001'
    #     }
    #     line_bot_api_error = LineBotApiError(
    #         status_code=409,
    #         request_id='123e4567-e89b-12d3-a456-426655440002',
    #         accepted_request_id='123e4567-e89b-12d3-a456-426655440001',
    #         headers=headers,
    #         error=Error(message='The retry key is already accepted')
    #     )
    #     self.assertEqual(
    #         line_bot_api_error.__str__(),
    #         'LineBotApiError: status_code=409, request_id=123e4567-e89b-12d3-a456-426655440002, '
    #         'accepted_request_id=123e4567-e89b-12d3-a456-426655440001, '
    #         'error_response={"details": [], "message": "The retry key is already accepted"}, '
    #         + 'headers={}'.format(headers)
    #     )


if __name__ == '__main__':
    unittest.main()