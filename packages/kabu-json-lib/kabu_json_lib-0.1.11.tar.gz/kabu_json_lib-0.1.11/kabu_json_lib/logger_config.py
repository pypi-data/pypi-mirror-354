#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
logger_config.py

このモジュールは、アプリケーション全体で使用する共通のロギング設定を提供します。
PythonのロガーはデフォルトでWARNINGレベルです。
"""

import logging
import sys
import json
import os


def setup_logger(name=None):
    """
    ロギングの基本設定を行います。

    Args:
        name (str, optional): ロガーの名前。デフォルトはNone（ルートロガー）。

    Returns:
        logging.Logger: 設定済みのロガーインスタンス
    """
    logger = logging.getLogger(name)

    # すでにハンドラーが設定されている場合は、重複を避けるために何もしない
    if logger.handlers:
        return logger

    # 環境変数からログレベルを取得（なければWARNING）
    level_str = os.getenv('LOG_LEVEL')
    default_level = logging.WARNING
    level = getattr(logging, (level_str or '').upper(),
                    default_level) if level_str else default_level

    # ロガーのレベルを設定
    logger.setLevel(level)

    # 日本語フォーマット
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        style='%'
    )

    # 標準出力へのハンドラー設定（INFOレベル以下）
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(level)
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    stdout_handler.terminator = '\n'
    logger.addHandler(stdout_handler)

    # 標準エラー出力へのハンドラー設定（WARNINGレベル以上）
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.terminator = '\n'
    logger.addHandler(stderr_handler)

    # propagateをFalseに設定して、親ロガーへの伝播を防ぐ
    logger.propagate = False

    return logger
