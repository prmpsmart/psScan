FROM python:3.9-slim
# Set the working directory inside the container to /app
WORKDIR /app
# Copy the requirements.txt file from the host to the container's working directory
COPY /src/requirements.txt ./
# Install the requirements specified in requirements.txt using pip
RUN pip install --no-cache-dir -r /requirements.txt
# Copy all the files from the host to the container's working directory
COPY . .
# Start the bot
CMD python3 src/bot.py
