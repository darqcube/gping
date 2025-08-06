# Globalping Traceroute Visualizer

A web application that visualizes traceroute data using the Globalping API with an interactive D3.js visualization.

## Features

- Interactive traceroute visualization with D3.js
- Filter routes by cumulative latency (Good, Medium, High)
- Hover tooltips showing IP addresses
- Organized layout with boxes arranged in lines
- Real-time traceroute measurements

## API Setup

Before running the application, you need to set up your Globalping API key:

1. **Get your API key**: Visit [https://globalping.io](https://globalping.io) and create an account
2. **Generate API key**: Go to your dashboard and create a new API key
3. **Create .env file**: Add your API key to a `.env` file in the project root:

```env
GLOBALPING_API_TOKEN=glp_your_actual_api_key_here
```

📖 **Detailed setup instructions**: See [API_SETUP.md](API_SETUP.md) for complete step-by-step guide.

## Docker Setup

### Quick Start with Docker Compose

1. **Build and run the container:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   Open your browser and go to `http://localhost:5001`

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Manual Docker Build

1. **Build the Docker image:**
   ```bash
   docker build -t globalping-traceroute .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 5001:5001 --name globalping-app globalping-traceroute
   ```

3. **Access the application:**
   Open your browser and go to `http://localhost:5001`

4. **Stop the container:**
   ```bash
   docker stop globalping-app
   docker rm globalping-app
   ```

## Environment Variables

You can set the following environment variables:

- `GLOBALPING_API_TOKEN`: Your Globalping API token (optional)
- `FLASK_ENV`: Set to `production` for production deployment

## Container Features

- **Auto-restart**: Container automatically restarts if it crashes
- **Health checks**: Built-in health monitoring
- **Security**: Runs as non-root user
- **Logging**: Unbuffered Python output for better logging
- **Port mapping**: Exposes port 5000

## Usage

1. Enter a target domain or IP address (e.g., `google.com`, `8.8.8.8`)
2. Click "Start Traceroute" to begin the measurement
3. Wait for the results to load
4. Use the filter buttons to view routes by cumulative latency:
   - **Good Total (<100ms)**: Routes with low cumulative latency
   - **Medium Total (100-500ms)**: Routes with moderate cumulative latency
   - **High Total (>500ms)**: Routes with high cumulative latency
5. Hover over boxes to see IP addresses
6. Drag boxes to reposition them

## Troubleshooting

### Container won't start
- Check if port 5001 is available: `netstat -tulpn | grep 5001`
- View container logs: `docker logs globalping-app`

### Application not responding
- Check container health: `docker ps`
- Restart container: `docker restart globalping-app`

### Build issues
- Clear Docker cache: `docker system prune -a`
- Rebuild without cache: `docker build --no-cache -t globalping-traceroute .`

## Development

For local development without Docker:

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```bash
   python globalping_traceroute.py
   ```

3. Access at `http://localhost:5001` 