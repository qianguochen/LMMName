#!/bin/bash

NUM_THREADS=64
PYTHON=python3
EXTRACTOR_JAR=jEdit_function/target/jEdit_function-1.0-SNAPSHOT.jar

${PYTHON} jEdit_function/extract.py  --num_threads ${NUM_THREADS} --contain_content --jar ${EXTRACTOR_JAR}

${PYTHON} jEdit_function/extract.py  --num_threads ${NUM_THREADS}  --jar ${EXTRACTOR_JAR}

