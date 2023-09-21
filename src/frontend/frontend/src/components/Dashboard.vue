<template>
	<head>
		<link
			rel="stylesheet"
			type="text/css"
			href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css"
		/>
	</head>
	<body>
		<!-- Primary Navigation Bar -->
		<div>
			<nav
				id="primaryNav"
				class="navbar bg-dark border-bottom border-bottom-dark"
				data-bs-theme="dark"
			>
				<div class="container-fluid">
					<router-link class="navbar-brand" to="/home"
						><img
							id="cm-logo"
							src="../assets/cm_logo_color_200.png"
							alt=""
						/>SDN Intrusion & Penetration System</router-link
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
					<ul class="nav nav-underline">
						<router-link to="/cve" class="nav-link">CVE Scan</router-link>
						<router-link to="/service" class="nav-link"
							>Service Scan</router-link
						>
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

			<div id="content" class="container">
				<label for="historyLog" class="form-label">History Log</label>
				<div id="historyOutputBox" class="card card-body">
					<table id="historyLogTable" class="table table-hover">
						<thead>
							<tr>
								<th scope="col">Type</th>
								<th scope="col">Date</th>
								<th scope="col">Time</th>
								<th scope="col">Target</th>
							</tr>
						</thead>
						<tbody>
							<tr
								v-for="activity in historyLog"
								:key="activity._id"
								@click="redirectToDetailPage(activity._id)"
							>
								<td>{{ activity.activity }}</td>
								<td>{{ activity.date }}</td>
								<td>{{ activity.time }}</td>
								<td v-if="activity.activity != 'IP SCAN MULTIPLE'">
									{{ activity.target }}
								</td>
								<td v-if="activity.activity === 'IP SCAN MULTIPLE'">
									<ul>
										<li v-for="(ip, index) in activity.target" :key="index">
											{{ ip }}
										</li>
									</ul>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</body>
</template>

<script>
import axios from "axios"
export default {
	name: "Dashboard",
	data() {
		return {
			historyLog: {},
		}
	},
	computed: {},
	methods: {
		getHistory() {
			const path = "http://127.0.0.1:5000/dashboard/history"
			axios
				.get(path)
				.then((res) => {
					console.log(res)
					this.historyLog = res.data
				})
				.catch((err) => {
					console.log(err)
				})
				.finally(() => {})
		},
		redirectToDetailPage(id) {
			// Use the `router-link` component to navigate to the detail page
			this.$router.push({ name: "historyDetail", params: { id } })
		},
	},
	mounted() {
		this.getHistory()
	},
}
</script>

<style scoped>
.navbar {
	height: 50px;
}
h1 {
	display: block;
}
.card-body {
	white-space: pre-wrap;
}
#historyOutputBox {
	margin-bottom: 50px;
}
#content {
	padding-top: 50px;
}
ul {
	list-style-type: none; /* Remove bullets */
	padding: 0; /* Remove padding */
}
</style>
