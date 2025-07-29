#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import logging
import os
from kabu_json_lib.logger_config import setup_logger
import uuid


def test_setup_logger_default():
    """デフォルト設定でのロガーテスト（デフォルトはWARNING）"""
    logger_name = f"test_logger_default_{uuid.uuid4()}"
    logger = setup_logger(logger_name)
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.WARNING
    assert len(logger.handlers) == 2


def test_setup_logger_custom_name():
    """カスタム名でのロガーテスト"""
    logger_name = f"test_logger_custom_{uuid.uuid4()}"
    logger = setup_logger(logger_name)
    assert logger.name == logger_name
    assert len(logger.handlers) == 2


def test_setup_logger_environment_level():
    """環境変数によるログレベルの設定テスト"""
    os.environ['LOG_LEVEL'] = 'DEBUG'
    logger_name = f"test_logger_env_{uuid.uuid4()}"
    logger = setup_logger(logger_name)
    assert logger.level == logging.DEBUG
    del os.environ['LOG_LEVEL']


def test_setup_logger_duplicate():
    """重複設定のテスト"""
    logger_name = f"duplicate_test_{uuid.uuid4()}"
    logger1 = setup_logger(logger_name)
    logger2 = setup_logger(logger_name)
    assert logger1 is logger2
    assert len(logger1.handlers) == 2
