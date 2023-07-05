# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock ./

# Copy the rest of the application code to the container
COPY . .

# Install the project dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Expose the port your application listens on
EXPOSE 8000

# Set the command to run your Python application using Poetry
CMD ["poetry", "run", "ipfsscrapper", "--configuration", "config.json"]
