FROM python:3.8.5

WORKDIR /app
COPY requirements.txt .
# RUN pip install Flask
RUN pip install -r requirements.txt
COPY . /app/

EXPOSE 5000

CMD [ "python", "run_coordinator.py" ]