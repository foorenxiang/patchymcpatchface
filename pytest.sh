#!/usr/bin/env bash
pytest tests/ -rvP \
--cov=. \
--cov-report html:cov_html \
--cov-report xml:coverage.xml \
--cov-report annotate:cov_annotate \