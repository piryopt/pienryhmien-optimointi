#!/bin/sh
python3 scripts/reset_test_db.py
tests/playwright/survey_testing.py --browser firefox