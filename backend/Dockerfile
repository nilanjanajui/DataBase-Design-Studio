FROM python:3.11-slim

# Install Graphviz — required by er_diagram.py (graphviz Python lib needs the system binary)
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend Python files (matches your exact project structure)
COPY app.py .
COPY cleanModify.py .
COPY convert_to_csv.py .
COPY dependency_preservation.py .
COPY er_diagram.py .
COPY fd_modified.py .
COPY key_utils.py .
COPY lossless_check.py .
COPY modifyMain.py .
COPY Normalize_1_2_3NF.py .
# NOTE: tempCodeRunnerFile.py is intentionally excluded — it's a VS Code artifact

# Create folders that app.py expects at runtime
RUN mkdir -p uploads processed

EXPOSE 5000

CMD ["python", "app.py"]