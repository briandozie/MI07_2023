<template>
	<div>
		<nav
			class="navbar bg-dark border-bottom border-bottom-dark"
			data-bs-theme="dark"
		>
			<div class="container-fluid">
				<router-link class="navbar-brand" to="/home"
					>SDN Intrusion & Penetration System</router-link
				>
				<a class="navbar-brand ms-auto" href="#">
					<i class="bi bi-gear"></i>
				</a>
				<a class="navbar-brand mS-auto" href="#">
					<i class="bi bi-person"></i>
				</a>
			</div>
		</nav>

		<nav class="navbar bg-secondary" data-bs-theme="dark">
			<div class="container-fluid navbar-expand">
				<div class="nav nav-underline">
					<router-link to="/cve" class="nav-link">CVE Scan</router-link>
					<router-link to="/service" class="nav-link">Service Scan</router-link>
					<router-link to="/ip" class="nav-link active">IP Scan</router-link>
					<router-link to="/port" class="nav-link">Port Scan</router-link>
					<router-link to="/dos" class="nav-link">DoS Attack</router-link>
					<router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
				</div>
			</div>
		</nav>

		<div class="container">
			<div id="topRow" class="row">
				<div class="col">
					<!-- Page Title -->
					<h1>IP Scan</h1>

					<form @submit="onSubmit">
						<!-- Target network input text field -->
						<div class="mb-3 w-75">
							<label for="inputValue" class="form-label">Target Network</label>
							<input
								type="text"
								class="form-control"
								id="inputValue"
								placeholder="IP range, multiple IP addresses, or a single IP address"
								v-model="ipScanForm.inputValue"
								@input="handleInput"
							/>
						</div>

						<div class="mb-3 w-75">
							<label for="inputValue" class="form-label">Subnet Mask</label>
							<input
								type="text"
								class="form-control"
								id="subnetMaskInput"
								placeholder="Subnet mask"
								v-model="ipScanForm.subnetMask"
							/>
						</div>

						<!-- Scan type dropdown menu -->
						<label for="scanTypeInput" class="form-label">Scan Type</label>
						<select
							class="form-select w-75"
							id="scanTypeInput"
							aria-label="Default select example"
							v-model="ipScanForm.scanType"
						>
							<option disabled value="">Select Scan Type</option>
							<option value="sn">TCP</option>
							<option value="sn">UDP</option>
						</select>

						<!-- Run button -->
						<div class="run-button">
							<button type="submit" class="btn btn-primary" :disabled="display">
								Run
							</button>
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
					<label for="resultOutput" class="form-label">Scan Result</label>
					<div id="resultOutputBox" class="card">
						<div class="card-body">{{ result }}</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios"

export default {
	name: "IPScan",
	data() {
		return {
			ipScanForm: {
				inputValue: "",
				ipRange: "",
				ipAddresses: "",
				ipAddress: "",
				subnetMask: "",
				scanType: "",
			},
			result: "",
			eventLog: "",
			display: false,
			isRunning: false,
			startTime: 0,
			elapsedTime: 0,
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
		scanIPs() {
			const input = this.ipScanForm.inputValue.trim()
			const ipAddresses = input.split(",").map((ip) => ip.trim())

			if (ipAddresses.length > 1) {
				// If there are multiple IP addresses, use the `ipAddresses` property in the payload.
				const payload = {
					ipAddresses: ipAddresses,
					subnetMask: this.ipScanForm.subnetMask,
					scanType: this.ipScanForm.scanType,
				}

				const path = "http://localhost:5000/ipScan/"
				this.startTimer() // start timer
				this.initStatus()
				this.display = true

				axios
					.post(path, payload)
					.then((res) => {
						console.log(res.data)
						this.result = res.data
						this.eventLog += `Scan completed successfully in ${this.formattedElapsedTimeEventLog}\n`
					})
					.catch((err) => {
						console.log(err)
					})
					.finally(() => {
						this.display = false
						this.stopTimer()
						this.resetTimer()
					})
			} else {
				// If it's not multiple IP addresses, follow the previous logic.
				let payload = {}

				if (input.includes("-")) {
					// If input contains a hyphen, it's an IP range.
					payload = { ipRange: input }
				} else {
					// Otherwise, it's a single IP address.
					payload = { ipAddress: input }
				}

				payload.subnetMask = this.ipScanForm.subnetMask
				payload.scanType = this.ipScanForm.scanType

				const path = "http://localhost:5000/ipScan/"
				this.startTimer() // start timer
				this.initStatus()
				this.display = true
				console.log(payload)
				axios
					.post(path, payload)
					.then((res) => {
						console.log(res.data)
						this.result = res.data
						this.eventLog += `Scan completed successfully in ${this.formattedElapsedTimeEventLog}\n`
					})
					.catch((err) => {
						console.log(err)
					})
					.finally(() => {
						this.display = false
						this.stopTimer()
						this.resetTimer()
					})
			}
		},

		// handleInput() {
		// 	const input = this.ipScanForm.inputValue.trim()

		// 	if (input.includes(",")) {
		// 		// If input contains a comma, it's multiple IP addresses.
		// 		this.ipScanForm.ipAddresses = input
		// 		this.ipScanForm.ipRange = ""
		// 		this.ipScanForm.ipAddress = ""
		// 	} else if (input.includes("-")) {
		// 		// If input contains a hyphen, it's an IP range.
		// 		const [startIP, endIP] = input.split("-")
		// 		this.ipScanForm.ipRange = `${startIP.trim()}-${endIP.trim()}`
		// 		this.ipScanForm.ipAddresses = ""
		// 		this.ipScanForm.ipAddress = ""
		// 	} else {
		// 		// Otherwise, it's a single IP address.
		// 		this.ipScanForm.ipAddress = input
		// 		this.ipScanForm.ipRange = ""
		// 		this.ipScanForm.ipAddresses = ""
		// 	}
		// },

		initForm() {
			this.ipScanForm.inputValue = ""
			this.ipScanForm.ipAddress = ""
			this.ipScanForm.ipRange = ""
			this.ipScanForm.ipAddresses = ""
			this.ipScanForm.subnetMask = ""
			this.ipScanForm.scanType = ""
		},
		initStatus() {
			this.eventLog = ""
			this.result = ""
		},
		onSubmit(e) {
			e.preventDefault()
			const payload = {
				inputValue: this.ipScanForm.inputValue,
				ipAddress: this.ipScanForm.ipAddress,
				ipRange: this.ipScanForm.ipRange,
				ipAddresses: this.ipScanForm.ipAddresses,
				subnetMask: this.ipScanForm.subnetMask,
				scanType: this.ipScanForm.scanType,
			}

			this.scanIPs(payload)
			this.initForm()
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
</style>
