from flask import Flask, render_template, request, jsonify
import requests
import json
import time
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

class GlobalpingTracer:
    def __init__(self, api_token=None):
        self.base_url = "https://api.globalping.io/v1"
        self.api_token = api_token or os.getenv("GLOBALPING_API_TOKEN")
        self.headers = {"Content-Type": "application/json"}
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"

    def get_probes(self, limit=50):
        """Get available probes from Globalping with diverse AS numbers"""
        try:
            response = requests.get(
                f"{self.base_url}/probes", params={"limit": limit}, headers=self.headers
            )
            if response.status_code == 200:
                probes = response.json()
                # Filter for unique AS numbers to ensure diverse paths
                as_numbers = set()
                unique_probes = []
                for probe in probes:
                    asn = probe.get("asn")
                    if asn and asn not in as_numbers:
                        as_numbers.add(asn)
                        unique_probes.append(probe)
                return unique_probes[:10]  # Limit to 10 diverse probes
            return []
        except Exception as e:
            print(f"Error fetching probes: {e}")
            return []

    def create_measurement(self, target, endpoint_location=None):
        """Create a traceroute measurement with predefined locations"""
        measurement_data = {
            "type": "traceroute",
            "target": target,
            "locations": [
                {"country": "PK", "city": "Karachi", "network": "aurologic GmbH"},
                {"country": "PK", "city": "Karachi", "network": "Zenlayer Inc"},
                {"country": "PK", "city": "Lahore", "network": "Pakistan Telecommunication Company Limited"},
                {"country": "PK", "city": "Islamabad", "network": "Virtury Cloud Private Limited"}
            ]
        }

        try:
            response = requests.post(
                f"{self.base_url}/measurements",
                json=measurement_data,
                headers=self.headers,
            )
            if response.status_code == 202:
                return response.json()
            else:
                print(f"Error creating measurement: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating measurement: {e}")
            return None

    def get_measurement_results(self, measurement_id, max_retries=30):
        """Get measurement results, polling until complete"""
        for _ in range(max_retries):
            try:
                response = requests.get(
                    f"{self.base_url}/measurements/{measurement_id}",
                    headers=self.headers,
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "finished":
                        return data
                    elif data.get("status") == "failed":
                        print(f"Measurement failed: {data}")
                        return None
                time.sleep(2)
            except Exception as e:
                print(f"Error fetching results: {e}")
                time.sleep(2)
        print("Measurement timed out")
        return None

    def parse_traceroute_results(self, results):
        """Parse traceroute results for visualization"""
        parsed_results = []
        for result in results.get("results", []):
            probe_info = result.get("probe", {})
            measurement_result = result.get("result", {})
            if measurement_result.get("status") != "finished":
                continue
            hops = []
            raw_output = measurement_result.get("rawOutput", "")
            lines = raw_output.split("\n")
            for line in lines:
                line = line.strip()
                if not line or line.startswith("traceroute"):
                    continue
                hop_match = re.match(r"^\s*(\d+)\s+(.+)", line)
                if hop_match:
                    hop_num = int(hop_match.group(1))
                    hop_data = hop_match.group(2).strip()
                    parts = hop_data.split()
                    if parts:
                        ip_or_host = parts[0]
                        times = [float(part.replace("ms", "")) for part in parts[1:] if part.replace(".", "").replace("ms", "").isdigit()]
                        avg_time = sum(times) / len(times) if times else 0
                        hops.append({"hop": hop_num, "ip": ip_or_host, "rtt": avg_time, "asn": probe_info.get("asn")})
            parsed_results.append({
                "probe": {
                    "country": probe_info.get("country"),
                    "city": probe_info.get("city"),
                    "network": probe_info.get("network"),
                    "latitude": probe_info.get("latitude"),
                    "longitude": probe_info.get("longitude"),
                    "asn": probe_info.get("asn")
                },
                "hops": hops,
            })
        return parsed_results

tracer = GlobalpingTracer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/traceroute", methods=["POST"])
def perform_traceroute():
    data = request.get_json()
    target = data.get("target")
    if not target:
        return jsonify({"error": "Target is required"}), 400
    measurement = tracer.create_measurement(target)
    if not measurement or not measurement.get("id"):
        return jsonify({"error": "Failed to create measurement"}), 500
    results = tracer.get_measurement_results(measurement["id"])
    if not results:
        return jsonify({"error": "Failed to get measurement results"}), 500
    parsed_results = tracer.parse_traceroute_results(results)
    return jsonify({"target": target, "results": parsed_results})

@app.route("/probes")
def get_probes():
    probes = tracer.get_probes()
    return jsonify(probes)

if __name__ == "__main__":
    app.run(debug=True, port=5001)