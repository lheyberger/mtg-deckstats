#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json


def _to_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def assert_objects_are_equal(result, expected):
    assert _to_json(result) == _to_json(expected)


def mock_response(requests_mock, pattern, response, basedir='tests/mocks'):
    if response:
        path = os.path.join(basedir, response)
        matcher = re.compile(pattern)
        with open(path, 'r', encoding='utf-8', newline='') as file:
            requests_mock.get(matcher, text=file.read())
        requests_mock.head(matcher, status_code=200)


def mock_responses(
        requests_mock,
        verb,
        pattern,
        responses,
        basedir='tests/mocks',
        ):
    response_list = []
    for response in responses:
        path = os.path.join(basedir, response)
        with open(path, 'r', encoding='utf-8', newline='') as file:
            response_list.append({'text': file.read()})
    matcher = re.compile(pattern)
    requests_mock.register_uri(verb, matcher, response_list)
    requests_mock.head(matcher, status_code=200)
