<template>
	<!-- Primary Navigation Bar -->
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

		<!-- Secondary Navigation Bar -->
		<nav class="navbar bg-secondary" data-bs-theme="dark">
			<div class="container-fluid navbar-expand">
				<div class="nav nav-underline">
					<router-link to="/cve" class="nav-link active">CVE Scan</router-link>
					<router-link to="/service" class="nav-link">Service Scan</router-link>
					<router-link to="/ip" class="nav-link">IP Scan</router-link>
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
					<h1>CVE Scan</h1>

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
								v-model="cveScanForm.ipAddress"
							/>
						</div>

						<!-- Scan type dropdown menu -->
						<label for="scanTypeInput" class="form-label">CVE Script</label>
						<select
							class="form-select w-75"
							id="scanTypeInput"
							aria-label="Default select example"
							v-model="cveScanForm.script"
						>
							<option disabled value="">Select CVE Script</option>
							<option value="vulners">Vulners</option>
							<option value="vuln">Vuln</option>
							<!-- <option value="sU">UDP</option> -->
						</select>

						<!-- Run button -->
						<div class="run-button">
							<button type="submit" class="btn btn-primary">Run</button>
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
						<div class="card-body">
							<!-- Call the method to render clickable links within the result -->
							<div v-html="renderClickableLinks(result)"></div>
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
	name: "CVEScan",
	data() {
		return {
			cveScanForm: {
				ipAddress: "",
				scanType: "sV",
				script: "",
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
		scanCVE(payload) {
			const path = "http://localhost:5000/cveScan/"
			this.startTimer() // start timer
			this.initStatus()
			this.eventLog += `Scan started on network "${this.cveScanForm.ipAddress}"\n`
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
		initForm() {
			this.cveScanForm.ipAddress = ""
			this.cveScanForm.scanType = "sV"
			this.cveScanForm.script = ""
		},
		initStatus() {
			this.eventLog = ""
			this.result = ""
		},
		onSubmit(e) {
			e.preventDefault()
			const payload = {
				ipAddress: this.cveScanForm.ipAddress,
				scanType: this.cveScanForm.scanType,
				script: this.cveScanForm.script,
			}
			console.log(payload)
			this.scanCVE(payload)
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
.custom-link {
	color: #007bff;
	text-decoration: underline;
	cursor: pointer;
}
.custom-link:hover {
	color: #0056b3;
}
</style>
