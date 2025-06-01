
FROM python:3.11

# 2️⃣ Set working directory inside the container
WORKDIR /app

# 3️⃣ Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Copy the rest of your code into the container
COPY . .

# 5️⃣ Expose port 5000 for Flask app
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--app", "app.main:app"]

