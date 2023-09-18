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
					<router-link to="/ip" class="nav-link">IP Scan</router-link>
					<router-link to="/port" class="nav-link">Port Scan</router-link>
					<router-link to="/dos" class="nav-link">DoS Attack</router-link>
					<router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
					<router-link to="/dashboard" class="nav-link active"
						>Dashboard</router-link
					>
				</div>
			</div>
		</nav>

		<div class="container">
			<label for="historyLog" class="form-label">History Details</label>
			<div class="card">
				<div class="row">
					<div class="col-4">
						<h1>Activity</h1>
						<p>{{ activity.activity }}</p>
						<h1>Type</h1>
						<p>{{ activity.type }}</p>
						<h1>Target Network</h1>
						<p>{{ activity.target }}</p>
					</div>
					<div class="col-8">
						<h1>Date</h1>
						<p>{{ activity.date }}</p>
						<h1>Time</h1>
						<p>{{ activity.time }}</p>
					</div>
				</div>
			</div>
		</div>
		<div id="results" class="container">
			<label for="historyLog" class="form-label">Results</label>
			<div class="card">
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
						<tr v-for="result in activity.result" :key="result.port">
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
</template>

<script>
import axios from "axios"
export default {
	name: "HistoryDetail",
	data() {
		return {
			activity: {},
		}
	},
	methods: {
		getHistoryDetails(id) {
			const path = `http://127.0.0.1:5000/dashboard/history/${id}`
			axios
				.get(path)
				.then((res) => {
					this.activity = res.data
				})
				.catch((err) => {
					console.log(err)
				})
				.finally(() => {})
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
	margin-left: 15px;
	padding-bottom: 50px;
}
#results {
	margin-bottom: 50px;
}
</style>
