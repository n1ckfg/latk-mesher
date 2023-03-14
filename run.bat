@echo off

cd %~dp0
python latk_mesher.py -- %1

@pause