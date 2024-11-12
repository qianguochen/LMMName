#!/bin/bash

PYTHON=python3


echo judge without method content
${PYTHON} judgment.py

echo judge with method content
${PYTHON} judgment.py --contain_content