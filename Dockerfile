# Stage 1: Build React Frontend
FROM node:20-alpine AS build-frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup Python Backend & Server
FROM python:3.11-slim
WORKDIR /app

# Install Python backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend static assets into Flask's static directory
COPY --from=build-frontend /app/frontend/dist ./static

EXPOSE 7860

# Set environment variables for Hugging Face Spaces
ENV PORT=7860
ENV FLASK_DEBUG=False

CMD ["python", "app.py"]
