<template>
	<!-- Primary Navigation Bar -->
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

		<!-- Secondary Navigation Bar -->
		<nav class="navbar bg-secondary" data-bs-theme="dark">
			<div class="container-fluid navbar-expand">
				<ul class="nav nav-underline">
					<router-link to="/cve" class="nav-link">CVE Scan</router-link>
					<router-link to="/service" class="nav-link">Service Scan</router-link>
					<router-link to="/ip" class="nav-link">IP Scan</router-link>
					<router-link to="/port" class="nav-link active"
						>Port Scan</router-link
					>
					<router-link to="/dos" class="nav-link">DoS Attack</router-link>
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
					<h1>Port Scan</h1>

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
								v-model="portScanForm.ipAddress"
							/>
							<!-- Display IP Address Error Message -->
							<div v-if="inputErrors.ipAddress" class="text-danger">
								{{ inputErrors.ipAddress }}
							</div>
						</div>

						<!-- Scan type dropdown menu -->
						<label for="scanTypeInput" class="form-label">Scan Type</label>
						<select
							class="form-select w-75"
							id="scanTypeInput"
							aria-label="Default select example"
							v-model="portScanForm.scanType"
						>
							<option disabled value="">Select Scan Type</option>
							<option value="TCP">TCP</option>
							<option value="UDP">UDP</option>
						</select>
						<!-- Display Scan Type Error Message -->
						<div v-if="inputErrors.scanType" class="text-danger">
							{{ inputErrors.scanType }}
						</div>

						<div class="button-container">
							<!-- Cancel Button -->
							<div class="run-button">
								<button
									@click="cancelActivity"
									class="btn btn-danger"
									v-if="display"
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
					<label for="resultOutput" class="form-label">Scan Result</label>
					<div class="card">
						<div class="card-body">
							<table id="outputTable" class="table table-hover">
								<thead>
									<tr>
										<th scope="col">Port</th>
										<th scope="col">Status</th>
										<th scope="col">Protocol</th>
										<th scope="col">Host</th>
									</tr>
								</thead>
								<tbody>
									<tr v-for="result in scanResult.ports" :key="result.port">
										<td>{{ result.port }}</td>
										<td>{{ result.status }}</td>
										<td>{{ result.protocol }}</td>
										<td>{{ result.host }}</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios"
import { getCurrentTimestamp } from "../shared/utilities.js"
export default {
	name: "PortScan",
	data() {
		return {
			portScanForm: {
				ipAddress: "",
				scanType: "",
			},
			inputErrors: {
				ipAddress: "",
				scanType: "",
			},
			scanResult: {},
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
		async scanPorts(payload) {
			const path = "http://127.0.0.1:5000/portScan/"
			this.startTimer() // start timer
			this.initStatus()
			const target = this.portScanForm.ipAddress
			this.eventLog +=
				getCurrentTimestamp() +
				` Scan started on network "${this.portScanForm.ipAddress}"\n`
			this.display = true

			try {
				const response = await axios.post(path, payload)
				if (response.status === 200) {
					this.scanResult = response.data
					this.eventLog +=
						getCurrentTimestamp() +
						` Scan completed successfully in ${this.formattedElapsedTimeEventLog}\n`
				}
			} catch (error) {
				this.eventLog +=
					getCurrentTimestamp() + ` Scan aborted: ${target} is not reachable\n`
			} finally {
				this.display = false
				this.stopTimer()
				this.resetTimer()
			}
		},
		// Error handling
		validateForm() {
			let isValid = true
			this.inputErrors = {} // Clear previous error messages

			if (!this.portScanForm.ipAddress.trim()) {
				this.inputErrors.ipAddress = "IP address is required."
				isValid = false
			} else if (!/^[\d.]+$/.test(this.portScanForm.ipAddress.trim())) {
				this.inputErrors.ipAddress = "Invalid IP address format."
				isValid = false
			}
			if (!this.portScanForm.scanType) {
				this.inputErrors.scanType = "Scan type is required."
				isValid = false
			}

			return isValid
		},
		initForm() {
			this.portScanForm.ipAddress = ""
			this.portScanForm.scanType = ""
		},
		initStatus() {
			this.eventLog = ""
			this.scanResult = ""
		},
		onSubmit(e) {
			e.preventDefault()
			if (this.validateForm()) {
				const payload = {
					ipAddress: this.portScanForm.ipAddress,
					scanType: this.portScanForm.scanType,
				}
				console.log(payload)
				this.scanPorts(payload)
				this.initForm()
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
#cm-logo {
	max-width: 100%;
	max-height: 100%;
	width: auto;
	height: auto;
	object-fit: cover;
	padding-right: 10px;
}
</style>
