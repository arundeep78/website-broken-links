#!/bin/bash
# read arguments from command prompt if there is no argument then run streamlit application
if [ -z "$1" ]; then

    streamlit run --server.address=0.0.0.0  /app/app.py
else
  exec "$@"
fi