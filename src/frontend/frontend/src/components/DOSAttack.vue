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
					<router-link to="/dos" class="nav-link active"
						>DoS Attack</router-link
					>
					<router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
				</ul>
				<ul class="nav nav-underline ms-auto">
					<router-link to="/dashboard" class="nav-link">Dashboard</router-link>
				</ul>
			</div>
		</nav>

		<div class="container">
			<div id="topRow" class="row">
				<div class="col">
					<!-- Page Title -->
					<h1>Denial-of-Service Attack</h1>

					<form @submit="onSubmit">
						<!-- Target network input text field -->
						<div class="mb-3 w-75">
							<label for="targetNetworkInput" class="form-label"
								>Target Network</label
							>
							<input
								type="text"
								class="form-control"
								id="targetNetworkInput"
								placeholder="IP address"
								v-model="dosAttackForm.ipAddress"
							/>
							<!-- Display IP Address Error Message -->
							<div v-if="inputErrors.ipAddress" class="text-danger">
								{{ inputErrors.ipAddress }}
							</div>
						</div>

						<!-- Target Port and Duration fields on the same line -->
						<div class="row mb-3 w-75">
							<div class="col-md-6">
								<!-- Target Port input text field -->
								<label for="targetPortInput" class="form-label"
									>Target Port</label
								>
								<input
									type="text"
									class="form-control"
									id="targetPortInput"
									placeholder="Port Number"
									v-model="dosAttackForm.portNumber"
								/>
								<!-- Display Port Number Error Message -->
								<div v-if="inputErrors.portNumber" class="text-danger">
									{{ inputErrors.portNumber }}
								</div>
							</div>
							<div class="col-md-6">
								<!-- Timeout input text field -->
								<label for="timeoutInput" class="form-label">Duration</label>
								<input
									type="text"
									class="form-control"
									id="timeoutInput"
									placeholder="Timeout (seconds)"
									v-model="dosAttackForm.duration"
								/>
								<!-- Display TimeOut Duration Error Message -->
								<div v-if="inputErrors.duration" class="text-danger">
									{{ inputErrors.duration }}
								</div>
							</div>
						</div>

						<!-- Attack type dropdown menu -->
						<label for="attackTypeInput" class="form-label">Attack Type</label>
						<select
							class="form-select w-75"
							id="attackTypeInput"
							aria-label="Default select example"
							v-model="dosAttackForm.attackType"
						>
							<option disabled value="">Select Attack Type</option>
							<option value="-S">SYN Flood</option>
							<option value="--udp">UDP Flood</option>
							<option value="--icmp">ICMP Flood</option>
						</select>
						<!-- Display Attack Type Error Message -->
						<div v-if="inputErrors.attackType" class="text-danger">
							{{ inputErrors.attackType }}
						</div>

						<!-- Target network input text field -->
						<div id="packetSize" class="mb-3 w-75">
							<label for="packetSizeInput" class="form-label"
								>Packet Size</label
							>
							<input
								type="text"
								class="form-control"
								id="packetSizeInput"
								placeholder="Number of bytes"
								v-model="dosAttackForm.packetSize"
							/>
							<!-- Display Packet Size Error Message -->
							<div v-if="inputErrors.packetSize" class="text-danger">
								{{ inputErrors.packetSize }}
							</div>
						</div>

						<div class="button-container">
							<!-- Cancel Button -->
							<div class="run-button">
								<button
									@click="cancelActivity"
									class="btn btn-danger"
									v-if="display"
									:disabled="isCancelled"
								>
									Cancel
								</button>
							</div>

							<!-- Run button -->
							<div class="run-button">
								<button
									type="submit"
									class="btn btn-primary"
									:disabled="display"
								>
									Run
								</button>
							</div>
						</div>
					</form>
				</div>
				<div class="col">
					<!-- Event Log -->
					<div class="row">
						<div class="col-md-4">
							<label for="eventLog" class="form-label">Event Log</label>
						</div>
						<div class="col-md-8">
							<div class="d-flex justify-content-between align-items-center">
								<!-- Progress Bar Column -->
								<div class="flex-grow-1">
									<div
										v-show="display"
										class="progress"
										role="progressbar"
										style="height: 10px"
									>
										<div
											class="progress-bar progress-bar-striped progress-bar-animated"
											style="width: 100%"
										></div>
									</div>
								</div>
								<!-- Text Column -->
								<div class="d-flex align-items-center ml-2">
									<!-- Timer -->
									<span v-show="display" id="timer">{{
										formattedElapsedTime
									}}</span>
								</div>
							</div>
						</div>
					</div>
					<div id="eventCard" class="card">
						<div id="eventLogBox" class="card-body">{{ eventLog }}</div>
					</div>
				</div>
			</div>
			<div id="bottomRow" class="row">
				<div class="col">
					<!-- Scan Result -->
					<label for="resultOutput" class="form-label">Network Latency</label>
					<div id="resultOutputBox" class="card">
						<div class="card-body">
							<div class="scrollable">
								{{ result }}
							</div>
						</div>
					</div>
				</div>
			</div>
			<div></div>
		</div>
	</div>
</template>

<script>
import { Chart, registerables } from "chart.js"
import axios from "axios"

Chart.register(...registerables)

export default {
	name: "DOSAttack",
	// components: { LineChart },

	data() {
		return {
			dosAttackForm: {
				ipAddress: "",
				portNumber: "",
				attackType: "",
				duration: "",
				packetSize: "",
			},
			inputErrors: {
				ipAddress: "",
				portNumber: "",
				attackType: "",
				duration: "",
				packetSize: "",
			},
			result: "",
			eventLog: "",
			display: false,
			isRunning: false,
			startTime: 0,
			elapsedTime: 0,
			isCancelled: false,
		}
	},
	computed: {
		formattedElapsedTime() {
			const minutes = Math.floor(this.elapsedTime / 60)
			const seconds = this.elapsedTime % 60
			return `${minutes.toString().padStart(2, "0")}:${seconds
				.toString()
				.padStart(2, "0")}`
		},
		formattedElapsedTimeEventLog() {
			const minutes = Math.floor(this.elapsedTime / 60)
			const seconds = this.elapsedTime % 60
			return `${minutes.toString().padStart(1, "0")} minute(s) and ${seconds
				.toString()
				.padStart(1, "0")} second(s)`
		},
	},
	methods: {
		// POST Function
		async dosAttack(payload) {
			const dosPath = "http://localhost:5000/dosAttack/"
			const latencyPath = "http://localhost:5000/dosAttack/latency"
			this.startTimer() // start timer
			this.initStatus()
			const target = this.dosAttackForm.ipAddress

			// update event log
			this.eventLog +=
				this.getCurrentTimestamp() +
				` DoS Attack (${payload.attackType}) started on network "${payload.ipAddress}" for ${payload.duration} second(s)"\n`
			this.eventLog +=
				this.getCurrentTimestamp() +
				` Flooding network with packets of ${payload.packetSize} data byte(s)\n`
			this.display = true
			const currentTime = new Date()
			const endTime = new Date(currentTime.getTime() + payload.duration * 1000)

			try {
				this.checkLatency(latencyPath, endTime) // poll for latency ping results
				await axios.post(dosPath, payload)

				if (this.isCancelled) {
					this.eventLog +=
						this.getCurrentTimestamp() +
						` DoS Attack cancelled manually after ${this.formattedElapsedTimeEventLog}\n`
				} else {
					this.eventLog +=
						this.getCurrentTimestamp() +
						` DoS Attack ended after ${this.formattedElapsedTimeEventLog}\n`
				}
				// poll for latency ping results
				this.checkLatency(latencyPath, endTime)
			} catch (err) {
				this.eventLog +=
					this.getCurrentTimestamp() +
					` DoS attack aborted: ${target} is not reachable\n`
			} finally {
				this.display = false
				this.initForm()
				this.stopTimer()
				this.resetTimer()
			}
		},
		checkLatency(latencyPath, endTime) {
			axios
				.post(latencyPath)
				.then((res) => {
					if (res.data.length > 0) {
						this.result += res.data + "\n"
					}
				})
				.catch((err) => {
					console.log(err)
				})
				.finally(() => {})

			// poll for latency ping results every 5 seconds
			if (new Date().getTime() < endTime.getTime() && !this.isCancelled) {
				setTimeout(this.checkLatency, 5000, latencyPath, endTime)
			}
			this.isCancelled = false
		},
		getCurrentTimestamp() {
			const now = new Date()
			const hours = now.getHours().toString().padStart(2, "0")
			const minutes = now.getMinutes().toString().padStart(2, "0")
			const seconds = now.getSeconds().toString().padStart(2, "0")

			return `[${hours}:${minutes}:${seconds}]`
		},
		validateForm() {
			let isValid = true
			this.inputErrors = {} // Clear previous error messages

			if (!this.dosAttackForm.ipAddress.trim()) {
				this.inputErrors.ipAddress = "IP address is required."
				isValid = false
			} else if (!/^[\d.]+$/.test(this.dosAttackForm.ipAddress.trim())) {
				this.inputErrors.ipAddress = "Invalid IP address format."
				isValid = false
			}

			if (!this.dosAttackForm.portNumber.trim()) {
				this.inputErrors.portNumber = "Port Number is required."
				isValid = false
			} else if (!/^\d+$/.test(this.dosAttackForm.portNumber)) {
				this.inputErrors.portNumber =
					"Port number must be a non-negative integer."
				isValid = false
			}

			if (!this.dosAttackForm.attackType) {
				this.inputErrors.attackType = "Attack type is required."
				isValid = false
			}

			if (!this.dosAttackForm.duration.trim()) {
				this.inputErrors.duration = "Time duration is required."
				isValid = false
			} else if (!/^\d+$/.test(this.dosAttackForm.duration)) {
				this.inputErrors.duration = "Duration must be a non-negative integer."
				isValid = false
			}

			if (!this.dosAttackForm.packetSize.trim()) {
				this.inputErrors.packetSize = "Packet size is required."
				isValid = false
			} else if (!/^\d+$/.test(this.dosAttackForm.packetSize)) {
				this.inputErrors.packetSize =
					"Packet size must be a non-negative integer."
				isValid = false
			}

			return isValid
		},
		initForm() {
			this.dosAttackForm.ipAddress = ""
			this.dosAttackForm.attackType = ""
			this.dosAttackForm.portNumber = ""
			this.dosAttackForm.duration = ""
			this.dosAttackForm.packetSize = ""
		},
		initStatus() {
			this.eventLog = ""
			this.result = ""
		},
		onSubmit(e) {
			e.preventDefault()
			if (this.validateForm()) {
				const payload = {
					ipAddress: this.dosAttackForm.ipAddress,
					portNumber: this.dosAttackForm.portNumber,
					attackType: this.dosAttackForm.attackType,
					attackTypeLabel:
						document.getElementById("attackTypeInput").options[
							document.getElementById("attackTypeInput").selectedIndex
						].textContent,
					duration: this.dosAttackForm.duration,
					packetSize: this.dosAttackForm.packetSize,
				}
				this.dosAttack(payload)
			}
		},
		startTimer() {
			if (!this.isRunning) {
				this.isRunning = true
				this.startTime = Date.now() - this.elapsedTime * 1000
				this.updateTimer()
			}
		},
		stopTimer() {
			if (this.isRunning) {
				this.isRunning = false
				clearInterval(this.timerInterval)
			}
		},
		resetTimer() {
			this.isRunning = false
			this.elapsedTime = 0
			clearInterval(this.timerInterval)
		},
		updateTimer() {
			this.timerInterval = setInterval(() => {
				this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000)
			}, 1000)
		},
		async cancelActivity(e) {
			e.preventDefault()
			this.isCancelled = true
			const cancelPath = "http://localhost:5000/dosAttack/cancel"

			try {
				this.eventLog +=
					this.getCurrentTimestamp() + ` Cancelling DoS Attack ...\n`
				await axios.get(cancelPath)
			} catch (err) {
				console.error(err)
			}
		},
	},
	created() {},
}
</script>

<style>
.navbar {
	height: 50px;
}
h1 {
	display: block;
}
form {
	padding-top: 30px;
	margin-left: 50px;
}
.btn-primary {
	min-width: 100px;
	max-width: 100px;
}
.run-button {
	padding-top: 53px;
	padding-right: 20px;
	text-align: right;
}
.card {
	min-height: 100px;
}
#topRow {
	padding-top: 50px;
}
#bottomRow {
	padding-top: 50px;
}
#packetSize {
	padding-top: 20px;
}
#eventCard {
	min-height: 300px;
	max-height: 300px;
}
.card-body {
	white-space: pre-wrap;
}
#resultOutputBox {
	margin-bottom: 50px;
}
#timer {
	text-align: right;
	padding-left: 15px;
}
.progress-bar-container {
	display: flex;
	align-items: center;
}
.progress-bar-container .progress {
	flex: 1;
}
.scrollable {
	overflow-y: auto;
	max-height: 300px;
}
#cm-logo {
	max-width: 100%;
	max-height: 100%;
	width: auto;
	height: auto;
	object-fit: cover;
	padding-right: 10px;
}
</style>
