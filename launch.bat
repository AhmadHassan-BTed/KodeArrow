@echo off
set /p ver=Select Version (S for Standard, R for R-Edition): 
if /i %ver%==S (python -m kode_arrow.versions.standard.main) else (python -m kode_arrow.versions.r_edition.main)
