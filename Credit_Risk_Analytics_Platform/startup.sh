#!/bin/bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev
pip install -r requirements.txt
streamlit run app.py --server.port 8000 --server.address 0.0.0.0
