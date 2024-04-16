FROM raviqqe/muffet AS build

FROM python:3.11.9-slim-bullseye

COPY requirements.txt /requirements.txt
# Install requirements
RUN pip install --no-cache-dir -r requirements.txt



COPY app /app


COPY --from=build /muffet /usr/bin/muffet


COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Expose port for Streamlit
EXPOSE 8501

ENTRYPOINT ["/entrypoint.sh"]
# CMD ["streamlit", "run", "--server.address=0.0.0.0", "--server.port=8052","/app/app.py"]
