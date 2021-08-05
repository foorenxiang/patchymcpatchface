#!/usr/bin/env bash
pytest test_patch.py -rvP \
--cov=. \
--cov-report html:cov_html \
--cov-report xml:coverage.xml \
--cov-report annotate:cov_annotate \