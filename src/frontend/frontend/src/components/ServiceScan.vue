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
					<router-link to="/cve" class="nav-link">CVE Scan</router-link>
					<router-link to="/Service" class="nav-link active"
						>Service Scan</router-link
					>
					<router-link to="/ip" class="nav-link">IP Scan</router-link>
					<router-link to="/port" class="nav-link">Port Scan</router-link>
					<router-link to="/dos" class="nav-link">DoS Attack</router-link>
					<router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
				</div>
			</div>
		</nav>

		<!-- Page Title -->
		<h1>Service Scan</h1>

		<form @submit="onSubmit">
			<!-- Target network input text field -->
			<div class="mb-3">
				<label for="targetNetworkInput" class="form-label"
					>Target Network</label
				>
				<input
					type="text"
					class="form-control"
					id="targetNetworkInput"
					placeholder="IP address"
					v-model="serviceScanForm.ipAddress"
				/>
			</div>

			<!-- Scan type dropdown menu -->
			<label for="scanTypeInput" class="form-label">Scan Type</label>
			<select
				class="form-select"
				id="scanTypeInput"
				aria-label="Default select example"
				v-model="serviceScanForm.scanType"
			>
				<option disabled value="">Select Scan Type</option>
				<option value="sV">TCP</option>
			</select>

			<!-- Run button -->
			<div class="run-button">
				<button type="submit" class="btn btn-primary">Run</button>
				<!-- <button type="submit" class="btn btn-primary float-end">Run</button> -->
			</div>
		</form>

		<!-- Scan Result -->
		<label for="resultOutput" class="form-label">Scan Result</label>
		<div class="card">
			<div class="card-body">{{ result }}</div>
		</div>
	</div>
</template>

<script>
import axios from "axios"
export default {
	name: "ServiceScan",
	data() {
		return {
			serviceScanForm: {
				ipAddress: "",
				scanType: "",
			},
			result: "",
		}
	},
	methods: {
		// POST Function
		scanServices(payload) {
			const path = "http://localhost:5000/serviceScan/"
			axios
				.post(path, payload)
				.then((res) => {
					console.log(res.data)
					this.result = res.data
				})
				.catch((err) => {
					console.log(err)
				})
		},
		initForm() {
			this.serviceScanForm.ipAddress = ""
			this.serviceScanForm.scanType = ""
		},
		onSubmit(e) {
			e.preventDefault()
			const payload = {
				ipAddress: this.serviceScanForm.ipAddress,
				scanType: this.serviceScanForm.scanType,
			}
			console.log(payload)
			this.scanServices(payload)
			this, this.initForm()
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
	padding-top: 10px;
	margin-left: 15px;
}
.btn-primary {
	min-width: 100px;
	max-width: 100px;
}
.run-button {
	padding-top: 50px;
	padding-bottom: 30px;
}
.card {
	min-height: 100px;
}
</style>
