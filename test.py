# Copied part of testing code in line-bot-sdk-python 
# licenced by: louis70109
# source: https://github.com/line/line-bot-sdk-python/blob/master/tests/test_exceptions.py

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


if __name__ == '__main__':
    unittest.main()