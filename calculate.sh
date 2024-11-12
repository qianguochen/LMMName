#!/bin/bash

PYTHON=python3
echo result without method content
${PYTHON} calculate_precision_recall.py
echo result with method content
${PYTHON} calculate_precision_recall.py --contain_content