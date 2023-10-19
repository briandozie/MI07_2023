<template>
	<div>
		<nav
			id="primaryNav"
			class="navbar bg-dark border-bottom border-bottom-dark"
			data-bs-theme="dark"
		>
			<div class="container-fluid">
				<router-link class="navbar-brand" to="/home"
					><img id="cm-logo" src="../assets/cm_logo_color_200.png" alt="" />SDN
					Intrusion & Penetration System</router-link
				>
				<div class="d-flex">
					<a class="navbar-brand ms-auto" href="/manual">
						<i class="bi bi-info-circle"></i>
					</a>
					<router-link class="navbar-brand ms-auto" to="/login">
						<i class="bi bi-box-arrow-right"></i> Logout
					</router-link>
				</div>
			</div>
		</nav>

		<nav class="navbar bg-secondary" data-bs-theme="dark">
			<div class="container-fluid navbar-expand">
				<ul class="nav nav-underline">
					<router-link to="/cve" class="nav-link">CVE Scan</router-link>
					<router-link to="/service" class="nav-link">Service Scan</router-link>
					<router-link to="/ip" class="nav-link">IP Scan</router-link>
					<router-link to="/port" class="nav-link">Port Scan</router-link>
					<router-link to="/dos" class="nav-link">DoS Attack</router-link>
					<router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
				</ul>
				<ul class="nav nav-underline ms-auto">
					<router-link to="/dashboard" class="nav-link active"
						>Dashboard</router-link
					>
				</ul>
			</div>
		</nav>

		<div class="container">
			<!-- Loading indicator -->
			<div v-if="isLoading" class="text-center mt-3">
				<div class="spinner-border" role="status">
					<span class="visually-hidden">Loading...</span>
				</div>
				<p>Loading...</p>
			</div>

			<label for="historyLog" class="form-label">History Details</label>
			<div class="card">
				<div class="row">
					<div class="col-4">
						<h1>Activity</h1>
						<p>{{ activity.activity }}</p>
						<h1>Type</h1>
						<p>{{ activity.type }}</p>
						<h1>Target Network</h1>
						<p v-if="activity.activity != 'IP SCAN MULTIPLE'">
							{{ activity.target }}
						</p>
						<ul v-if="activity.activity === 'IP SCAN MULTIPLE'">
							<li v-for="(ip, index) in activity.target" :key="index">
								{{ ip }}
							</li>
						</ul>
					</div>
					<div v-if="dosAttack" class="col-4">
						<h1>Duration</h1>
						<p>{{ activity.duration }} second(s)</p>
						<h1>Packet Size</h1>
						<p>{{ activity.packetSize }} byte(s)</p>
						<h1>Target Port</h1>
						<p>{{ activity.port }}</p>
					</div>
					<div class="col-4">
						<h1>Date</h1>
						<p>{{ activity.date }}</p>
						<h1>Time</h1>
						<p>{{ activity.time }}</p>
					</div>
				</div>
			</div>
		</div>
		<div id="results" class="container">
			<label v-if="!dosAttack" for="historyLog" class="form-label"
				>Results</label
			>
			<div v-if="!dosAttack" id="resultCard" class="card">
				<!-- CVE Scan Result Table -->
				<table v-if="cveScan" class="table table-hover">
					<thead>
						<tr>
							<th>Port</th>
							<th>State</th>
							<th>Service</th>
							<th>CVEs</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(entry, index) in cveScanResult" :key="index">
							<td>{{ entry.port }}</td>
							<td>{{ entry.state }}</td>
							<td>{{ entry.service }}</td>
							<td>
								<ul>
									<!-- Iterate through the cve list of each port -->
									<li v-for="(cve, cveIndex) in entry.cves" :key="cveIndex">
										<a :href="cve.link" target="_blank">{{ cve.id }}</a>
									</li>
								</ul>
							</td>
						</tr>
					</tbody>
				</table>

				<!-- Service Scan Result Table -->
				<table v-if="serviceScan" id="outputTable" class="table table-hover">
					<thead>
						<tr>
							<th scope="col">Host</th>
							<th scope="col">Port</th>
							<th scope="col">Name</th>
							<th scope="col">Product</th>
							<th scope="col">Extra Info</th>
							<th scope="col">Version</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="result in activity.result" :key="result.port">
							<td>{{ result.host }}</td>
							<td>{{ result.port }}</td>
							<td>{{ result.name }}</td>
							<td>{{ result.product }}</td>
							<td>{{ result.extrainfo }}</td>
							<td>{{ result.version }}</td>
						</tr>
					</tbody>
				</table>

				<!-- IP Scan Result Table -->
				<table v-if="ipScan" id="outputTable" class="table table-hover">
					<thead>
						<tr>
							<th scope="col">IP</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="result in activity.result" :key="result">
							<td>{{ result }}</td>
						</tr>
					</tbody>
				</table>

				<!-- Port Scan Result Table -->
				<table v-if="portScan" id="outputTable" class="table table-hover">
					<thead>
						<tr>
							<th scope="col">Port</th>
							<th scope="col">Status</th>
							<th scope="col">Protocol</th>
							<th scope="col">Host</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="result in activity.result" :key="result.port">
							<td>{{ result.port }}</td>
							<td>{{ result.status }}</td>
							<td>{{ result.protocol }}</td>
							<td>{{ result.host }}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<!-- Network Latency Results Box -->
			<div v-if="dosAttack">
				<label for="resultOutput" class="form-label">Network Latency</label>
				<div id="resultOutputBox" class="card">
					<div class="card-body">
						<div class="scrollable">
							{{ latencyResult }}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios"
export default {
	name: "HistoryDetail",
	data() {
		return {
			isLoading: false,
			activity: {},
			cveScanResult: [],
			latencyResult: "",
			portScan: false,
			cveScan: false,
			serviceScan: false,
			ipScan: false,
			dosAttack: false,
		}
	},
	methods: {
		getHistoryDetails(id) {
			const path = `http://127.0.0.1:5000/dashboard/history/${id}`
			this.isLoading = true // Show loading indicator
			axios
				.get(path)
				.then((res) => {
					this.activity = res.data
					console.log("activity contents", this.activity)
					switch (this.activity.activity) {
						case "PORT SCAN":
							this.portScan = true
							break
						case "CVE SCAN":
							this.cveScan = true
							this.parseCveScanOutput()
							break
						case "SERVICE SCAN":
							this.serviceScan = true
							break
						case "IP SCAN SINGLE":
						case "IP SCAN MULTIPLE":
						case "IP SCAN RANGE":
							this.ipScan = true
							break
						case "DOS ATTACK":
						case "DDOS ATTACK":
							this.dosAttack = true
							this.parseNetworkLatencyOutput()
							break
					}
				})
				.catch((err) => {
					console.log(err)
				})
				.finally(() => {
					this.isLoading = false
				})
		},
		// Method to identify links in output using regular expression
		renderClickableLinks(text) {
			const urlPattern = /https?:\/\/[^\s/$.?#].[^\s]*/gi

			//Replace URLs with anchor elements
			const resultWithLinks = text.replace(urlPattern, (url) => {
				return `<a class="custom-link" href="${url}" target="_blank">${url}</a>`
			})

			return resultWithLinks
		},
		// Method to parse the output into Arrays
		parseCveScanOutput() {
			const lines = this.activity.result.split("\n")
			let currentEntry = {}

			for (const line of lines) {
				const parts = line.split(/\s+/)
				if (parts.length >= 3 && parts[0].endsWith("/tcp")) {
					//If current entry has data, push it to the array
					//before starting a new one
					if (Object.keys(currentEntry).length > 0) {
						this.cveScanResult.push(currentEntry)
					}

					// Start a new entry
					currentEntry = {
						port: parts[0],
						state: parts[1],
						service: parts[2],
						cves: [],
					}
				} else if (line.match(/https?:\/\/vulners\.com\/cve\/\S+/)) {
					// Parse CVE lines
					const cveParts = line.split(/\s+/)
					const cveId = cveParts[1]
					const cveLink = cveParts[3]
					currentEntry.cves.push({ id: cveId, link: cveLink })
				} else if (line.match(/https?:\/\/cve\.mitre\.org\/\S+/)) {
					// Parse links from http://cve.mitre.org/
					const cveParts = line.split(/\s+/)
					const cveDesc = "Mitre Link" //Placeholder Description
					const cveLink = cveParts[1]
					currentEntry.cves.push({ id: cveDesc, link: cveLink })
				} else if (line.match(/https?:\/\/seclists\.org\/\S+/)) {
					// Parse links from http://seclists.org/
					const cveParts = line.split(/\s+/)
					const cveDesc = "SecLists Link" //Placeholder Description
					const cveLink = cveParts[1]
					currentEntry.cves.push({ id: cveDesc, link: cveLink })
				}
			}

			// Push the last entry to the result array once the loop ends
			if (Object.keys(currentEntry).length > 0) {
				this.cveScanResult.push(currentEntry)
			}
			console.log("cveScanResult:", this.cveScanResult)
		},
		parseNetworkLatencyOutput() {
			for (let i = 0; i < this.activity.result.length; i++) {
				this.latencyResult += this.activity.result[i] + "\n"
			}
		},
	},
	mounted() {
		this.getHistoryDetails(this.$route.params.id)
	},
}
</script>

<style scoped>
.navbar {
	height: 50px;
}
p {
	display: block;
	padding-top: 0px;
	margin-left: 15px;
}
.container {
	padding-top: 50px;
}
h1 {
	padding-top: 10px;
	margin-left: 15px;
	font-size: 30px !important;
}
table {
	padding-top: 10px;
	padding-bottom: 50px;
}
#results {
	margin-bottom: 50px;
}
#resultCard {
	padding-top: 5px;
	padding-left: 15px;
	padding-right: 15px;
}
</style>
