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
					<a class="navbar-brand ms-auto" href="#">
						<i class="bi bi-gear"></i>
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
					<router-link to="/ip" class="nav-link active">IP Scan</router-link>
					<router-link to="/port" class="nav-link">Port Scan</router-link>
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
					<h1>IP Scan</h1>
					<!-- Button Group -->
					<div
						class="btn-group btn-group-sm"
						role="group"
						aria-label="Small button group"
					>
						<!-- Single IP Button Group -->
						<input
							type="radio"
							class="btn-check"
							name="btnradio"
							id="btnradio1"
							autocomplete="off"
							v-model="selectedRadio1"
							value="btnradio1"
							@change="setDefaultInputVisibility"
						/>
						<label class="btn btn-outline-primary" for="btnradio1"
							>Single IP</label
						>
						<!-- Multiple IP Button Group -->
						<input
							type="radio"
							class="btn-check"
							name="btnradio"
							id="btnradio2"
							autocomplete="off"
							v-model="selectedRadio2"
							value="btnradio2"
							@change="handleInputRadioChange2"
						/>

						<label class="btn btn-outline-primary" for="btnradio2"
							>Multiple IP</label
						>
						<!-- IP Range Button Group -->
						<input
							type="radio"
							class="btn-check"
							name="btnradio"
							id="btnradio3"
							autocomplete="off"
							v-model="selectedRadio3"
							value="btnradio3"
							@change="handleInputRadioChange3"
						/>
						<label class="btn btn-outline-primary" for="btnradio3"
							>IP Range</label
						>
					</div>

					<form @submit="onSubmit">
						<!-- Target network input text field  v-if="selectedRadio === 'btnradio1'" -->
						<div class="mb-3 w-75">
							<label for="inputValue1" class="form-label">Target Network</label>
							<!-- For Single IP Only -->
							<input
								type="text"
								class="form-control"
								id="inputValue1"
								placeholder="Single IP address"
								v-model="ipScanForm.inputValue1"
								@input="handleInputRadioChange1"
								v-if="showInputField1"
							/>
							<div
								class="error-message text-danger"
								v-if="showInputField1 && errors.inputValue1"
							>
								{{ errors.inputValue1 }}
							</div>
							<!-- For Multiple IP Only -->
							<div class="input-group">
								<input
									type="text"
									class="form-control"
									id="inputValue2"
									placeholder="IP address"
									v-model="ipScanForm.inputValue2"
									@input="handleInputRadioChange2"
									v-if="showInputField2"
								/>

								<!-- Button to add new input field -->
								<div class="input-group-append" v-if="showInputField2">
									<button
										class="btn btn-outline-primary"
										@click.prevent="addIPInput"
									>
										+
									</button>
								</div>
							</div>
							<!-- New input field -->
							<div
								v-for="(input, index) in ipScanForm.additionalInputs"
								:key="index"
								class="input-group mb-1"
							>
								<input
									type="text"
									class="form-control mt-1"
									v-model="ipScanForm.additionalInputs[index]"
									placeholder="IP address"
								/>
								<!-- Button to delete input field -->
								<div class="input-group-append mt-1">
									<button
										type="button"
										class="btn-close mt-1"
										@click="removeIPInput(index)"
									/>
								</div>
							</div>
							<div
								class="error-message text-danger"
								v-if="showInputField2 && errors.inputValue2"
							>
								{{ errors.inputValue2 }}
							</div>
							<!-- For IP Range Only -->
							<div class="input-group mb-3">
								<input
									type="text"
									class="form-control"
									id="inputValueStart"
									placeholder="Start IP"
									v-model="ipScanForm.inputStart"
									@input="handleInputRadioChange3"
									v-if="showInputField3"
								/>
								<!-- Separate StartIP and EndIP -->
								<span class="input-group-text" v-if="showInputField3">-</span>
								<input
									type="text"
									class="form-control"
									id="inputValueEnd"
									placeholder="End IP"
									v-model="ipScanForm.inputEnd"
									@input="handleInputRadioChange3"
									v-if="showInputField3"
								/>
							</div>
							<div
								class="error-message text-danger"
								v-if="showInputField3 && errors.inputStart"
							>
								{{ errors.inputStart }}
							</div>
							<div
								class="error-message text-danger"
								v-if="showInputField3 && errors.inputEnd"
							>
								{{ errors.inputEnd }}
							</div>
						</div>

						<!-- Subnet Mask-->
						<div class="mb-3 w-75" v-if="showInputField1">
							<label for="inputValue" class="form-label">Subnet Mask</label>
							<input
								type="text"
								class="form-control"
								id="subnetMaskInput"
								placeholder="Subnet mask"
								v-model="ipScanForm.subnetMask"
							/>
							<div
								class="error-message text-danger"
								v-if="showInputField1 && errors.subnetMask"
							>
								{{ errors.subnetMask }}
							</div>
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
							<option value="sS">TCP SYN (Stealth)</option>
						</select>
						<div class="error-message text-danger" v-if="errors.scanType">
							{{ errors.scanType }}
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
										<th scope="col">IP</th>
									</tr>
								</thead>
								<tbody>
									<tr v-for="result in scanResult" :key="result">
										<td>{{ result }}</td>
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
	name: "IPScan",
	data() {
		return {
			ipScanForm: {
				inputValue1: "",
				inputValue2: "",
				inputStart: "",
				inputEnd: "",
				additionalInputs: [],
				subnetMask: "",
				scanType: "",
				selectedRadio2: "btnradio2",
				selectedRadio3: "btnradio3",
				errorMessage: null,
			},
			errors: {
				inputValue1: null,
				inputValue2: null,
				inputStart: null,
				inputEnd: null,
				subnetMask: null,
				scanType: null,
			},
			scanResult: "",
			eventLog: "",
			display: false,
			isRunning: false,
			startTime: 0,
			elapsedTime: 0,

			selectedRadio1: "btnradio1",
			showInputField1: true,
			showInputField2: true,
			showInputField3: true,
		}
	},

	computed: {
		isFormValid() {
			const isValid =
				(this.errors.inputValue1 === null &&
					this.errors.scanType === null &&
					this.errors.subnetMask === null) ||
				(this.errors.inputValue2 === null && this.errors.scanType === null) ||
				(this.errors.inputStart === null &&
					this.errors.inputEnd === null &&
					this.errors.scanType === null)
			return isValid
		},
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
		validateInputValue1() {
			const inputValue1 = this.ipScanForm.inputValue1.trim()
			if (!inputValue1) {
				this.errors.inputValue1 = "Ip address is required."
			} else if (!/^\d+(\.\d+)*$/.test(inputValue1)) {
				this.errors.inputValue1 = "Invalid IP address format."
			} else {
				this.errors.inputValue1 = null // No error
			}
		},
		validateInputValue2() {
			// Multiple Ip
			const inputValue2 = this.ipScanForm.inputValue2.trim()
			if (!inputValue2) {
				this.errors.inputValue2 = "Ip address is required."
			} else if (!/^\d+(\.\d+)*$/.test(inputValue2)) {
				this.errors.inputValue2 = "Invalid IP address format."
			} else {
				this.errors.inputValue2 = null // No error
			}
		},
		validateInputStart() {
			const inputStart = this.ipScanForm.inputStart.trim()
			if (!inputStart) {
				this.errors.inputStart = "Ip address is required."
			} else if (!/^\d+(\.\d+)*$/.test(inputStart)) {
				this.errors.inputStart = "Invalid IP address format."
			} else {
				this.errors.inputStart = null // No error
			}
		},
		validateInputEnd() {
			const inputEnd = this.ipScanForm.inputEnd.trim()
			if (!inputEnd) {
				this.errors.inputEnd = "Ip address is required."
			} else if (!/^\d+(\.\d+)*$/.test(inputEnd)) {
				this.errors.inputEnd = "Invalid IP address format."
			} else {
				this.errors.inputEnd = null // No error
			}
		},
		validateInputSM() {
			// subnet mask
			const subnetMask = this.ipScanForm.subnetMask.trim()
			if (!subnetMask) {
				this.errors.subnetMask = "Subnet mask is required."
			} else if (!/^\d+(\.\d+)*$/.test(subnetMask)) {
				this.errors.subnetMask = "Invalid subnet mask format."
			} else {
				this.errors.subnetMask = null // No error
			}
		},
		validateInputST() {
			if (!this.ipScanForm.scanType.trim()) {
				this.errors.scanType = "Scan type is required."
			} else {
				this.errors.scanType = null // No error
			}
		},
		resetForm() {
			this.scanResult = ""
			this.eventLog = ""
			this.ipScanForm.additionalInputs = []
		},

		setDefaultInputVisibility() {
			if (this.selectedRadio1 === "btnradio1") {
				this.showInputField1 = true
				this.showInputField2 = false
				this.showInputField3 = false

				this.ipScanForm.inputStart = ""
				this.ipScanForm.inputEnd = ""
				this.ipScanForm.inputValue2 = ""
				this.ipScanForm.additionalInputs = []
				this.errors.inputValue1 = null
				this.errors.inputValue2 = null
				this.errors.inputStart = null
				this.errors.inputEnd = null
				this.errors.subnetMask = null
				this.errors.scanType = null
				this.resetForm()
			} else {
				this.showInputField1 = false
			}
		},
		handleInputRadioChange2() {
			if (this.selectedRadio2 === "btnradio2") {
				this.showInputField2 = true
				this.showInputField1 = false
				this.showInputField3 = false
				if (this.ipScanForm.additionalInputs.length > 0) {
					this.ipScanForm.inputValue2 = this.ipScanForm.additionalInputs[0]
					this.ipScanForm.additionalInputs.splice(0, 1)
				}
				this.ipScanForm.inputValue1 = ""
				this.ipScanForm.inputStart = ""
				this.ipScanForm.inputEnd = ""
				this.errors.inputValue1 = null
				this.errors.inputValue2 = null
				this.errors.inputStart = null
				this.errors.inputEnd = null
				this.errors.subnetMask = null
				this.errors.scanType = null
				this.resetForm()
			} else {
				this.showInputField2 = false
			}
		},

		handleInputRadioChange3() {
			if (this.selectedRadio3 === "btnradio3") {
				this.showInputField3 = true
				this.showInputField1 = false
				this.showInputField2 = false
				this.ipScanForm.inputValue1 = ""
				this.ipScanForm.inputValue2 = ""
				this.ipScanForm.additionalInputs = []
				this.errors.inputValue1 = null
				this.errors.inputValue2 = null
				this.errors.inputStart = null
				this.errors.inputEnd = null
				this.errors.subnetMask = null
				this.errors.scanType = null
				this.resetForm()
			} else {
				this.showInputField3 = false
			}
		},

		// POST Function
		scanIPs() {
			const input1 = this.ipScanForm.inputValue1.trim()
			const input2 = this.ipScanForm.inputValue2.trim()
			const start = this.ipScanForm.inputStart.trim()
			const end = this.ipScanForm.inputEnd.trim()
			// if (!input1 && !input2 && !start && !end) {
			// 	// No valid input provided, display an error message instead of starting the scan.
			// 	this.eventLog +=
			// 		"No valid input provided. Please enter an IP address or range.\n"
			// 	return
			// }
			let payload = {}

			if (start && end) {
				payload = {
					ipRange: `${start}-${end}`,
				}
			} else if (input1) {
				// single IP address.
				payload = { ipAddress: input1 }
			} else if (input2) {
				const ipAddresses = input2.split(",").map((ip) => ip.trim())

				if (this.selectedRadio2 === "btnradio2") {
					const additionalIPs = this.ipScanForm.additionalInputs.filter(
						(ip) => ip.trim() !== ""
					)
					payload = { ipAddresses: [...ipAddresses, ...additionalIPs] }
				} else {
					payload = { ipAddresses }
				}
			} else {
				console.error("Invalid input provided.")
			}
			const ipInfo = payload.ipRange || payload.ipAddress || payload.ipAddresses
			payload.subnetMask = this.ipScanForm.subnetMask
			payload.scanType = this.ipScanForm.scanType
			payload.scanTypeLabel =
				document.getElementById("scanTypeInput").options[
					document.getElementById("scanTypeInput").selectedIndex
				].textContent

			const path = "http://localhost:5000/ipScan/"
			this.startTimer()
			this.initStatus()
			this.eventLog +=
				getCurrentTimestamp() + ` Scan started on network "${ipInfo}"\n`
			this.display = true
			console.log(payload)
			axios
				.post(path, payload)
				.then((res) => {
					console.log(res.data)
					if (res.status === 200) {
						this.scanResult = res.data
						this.eventLog +=
							getCurrentTimestamp() +
							` Scan completed successfully in ${this.formattedElapsedTimeEventLog}\n`
					}
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

		initForm() {
			this.ipScanForm.inputValue1 = ""
			this.ipScanForm.inputValue2 = ""
			this.ipScanForm.inputStart = ""
			this.ipScanForm.inputEnd = ""
			this.ipScanForm.subnetMask = ""
			this.ipScanForm.scanType = ""
			this.ipScanForm.additionalInputs = []
		},
		initStatus() {
			this.eventLog = ""
			this.scanResult = ""
		},
		onSubmit(e) {
			e.preventDefault()

			// Validate the form inputs
			this.validateInputValue1()
			this.validateInputValue2()
			this.validateInputStart()
			this.validateInputEnd()
			this.validateInputSM()
			this.validateInputST()

			// Check if the form is valid
			if (this.isFormValid) {
				// Proceed with the IP scan
				const payload = {
					inputValue1: this.ipScanForm.inputValue1,
					inputValue2: this.ipScanForm.inputValue2,
					inputStart: this.ipScanForm.inputStart,
					inputEnd: this.ipScanForm.inputEnd,
					subnetMask: this.ipScanForm.subnetMask,
					scanType: this.ipScanForm.scanType,
				}
				this.scanIPs(payload)
				this.initForm()
			} else {
				// The form is invalid, do not proceed with the scan
				console.log("Form is invalid. Please correct the errors.")
			}

			// const payload = {
			// 	inputValue1: this.ipScanForm.inputValue1,
			// 	inputValue2: this.ipScanForm.inputValue2,
			// 	inputStart: this.ipScanForm.inputStart,
			// 	inputEnd: this.ipScanForm.inputEnd,
			// 	subnetMask: this.ipScanForm.subnetMask,
			// 	scanType: this.ipScanForm.scanType,
			// }
			// this.scanIPs(payload)
			// this.initForm()
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
		addIPInput() {
			this.ipScanForm.additionalInputs.push("")
		},
		removeIPInput(index) {
			this.ipScanForm.additionalInputs.splice(index, 1)
		},
		cancelActivity(e) {
			e.preventDefault()
			const cancelPath = "http://localhost:5000/ipScan/cancel"
			axios
				.get(cancelPath)
				.then((res) => {
					if (res.status === 200) {
						this.eventLog +=
							getCurrentTimestamp() +
							` Scan cancelled manually after ${this.formattedElapsedTimeEventLog}\n`
					}
				})
				.catch((err) => {
					console.log(err)
				})
		},
	},
	created() {
		this.setDefaultInputVisibility()
	},
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
