#!/bin/bash
# Start the application

version="2024-07-27v1"

echo "####################"
echo "# Starting FastAPI #"
echo "####################"
echo 
echo Generate from https://github.com/solufit/fastapi-template
echo Version: $version
echo Copyright 2024 Solufit All Right Reserved
echo This software is released under the MIT License.
echo http://opensource.org/licenses/mit-license.php
echo 
echo ------------------------------------------------
echo Step1: Update Database Model
echo

alembic upgrade head

# Check the command exited correctly
if [ $? -gt 0 ]; then
    echo Error: Failed to update database model
    exit 1
fi

echo
echo ------------------------------------------------
echo Step2: Start FastAPI Server
echo

uvicorn src:app --reload --host 0.0.0.0 --port 5000