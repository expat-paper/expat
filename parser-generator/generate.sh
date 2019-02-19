#!/bin/bash

antlr4='java -jar /usr/local/lib/antlr-4.7.1-complete.jar'
$antlr4 -visitor -Dlanguage=Python3 OPOL.g4
