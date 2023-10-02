
# Choosing an image for you container.
FROM python:3.9-slim
# FROM python:3.11.0

# Set the working directory inside the container to /app
WORKDIR /app

# This command would copy EVERY FILE from your project folder into your container, so be careful.
COPY . .

# Installing needed packages and dependencies.**
RUN pip install -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

# Start the application using uvicorn with the specified host and port
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "8000"]
