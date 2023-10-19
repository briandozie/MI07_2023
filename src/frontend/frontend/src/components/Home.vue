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

		<nav id="secondaryNav" class="navbar bg-secondary" data-bs-theme="dark">
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
					<router-link to="/dashboard" class="nav-link">Dashboard</router-link>
				</ul>
			</div>
		</nav>

		<div class="row container">
			<div class="col col-left">
				<img id="image" src="../assets/pic.jpg" alt="" />
			</div>
			<div class="col">
				<div id="padd">
					<p>WELCOME,</p>
					<h1 class="admin-section">ADMIN</h1>
					<div>
						<br />
						<h3 class="message">
							Software-Defined Intrusion and Penetration System
						</h3>
						<p3>
							The project is a software-based intrusion and penetration testing
							system that can be used to target and identify vulnerabilities in
							Industrial Control Systems (ICS) utilizing Software-Defined
							Networking (SDN) framework.
						</p3>
					</div>
					<div id="button">
						<button
							type="submit"
							class="btn btn-primary"
							@click="navigateToManual"
						>
							Learn More
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	methods: {
		navigateToManual() {
			// Use $router.push to navigate to another route
			this.$router.push("/manual")
		},
	},
}
</script>

<style scoped>
body {
	overflow-x: hidden;
}
.col {
	margin: 0;
	padding: 0;
}
.container {
	max-width: 100%;
	min-height: 100vh;
	height: 100%;
}
.col-left {
	flex: 1.5;
	display: flex;
	align-items: stretch;
	overflow: hidden; /* Ensure that no content overflows and causes extra space */
}

#image {
	width: 100%;
	height: 100%;
	object-fit: cover;
	object-position: top; /* Align the top of the image */
}

#padd {
	padding: 200px 80px 0px 80px;
}
.card {
	padding: 0;
	margin: 0;
	height: 80px;
}
.spacer {
	height: 20px;
}

#topRow {
	width: 100%;
	overflow: hidden;
	height: 600px;
}
.message {
	text-align: right;
	margin-top: 20px;
	margin-left: 100px;
}
#cm-logo {
	max-width: 100%;
	max-height: 100%;
	width: auto;
	height: auto;
	object-fit: cover;
	padding-right: 10px;
}

.pad {
	margin-left: 60px;
}

#primaryNav {
	height: 80px;
}
p {
	display: block;
	/* padding-top: 100px; */
}
p2 {
	text-align: right;
	display: block;
	padding-top: 10px;
	margin-left: 100px;
}

p3 {
	text-align: right;
	display: block;
	padding-top: 20px;
	margin-left: 100px;
}
.navbar-brand.ms-auto {
	color: #fff; /* Text color */
	text-decoration: none; /* Remove underline */
	cursor: pointer; /* Change cursor on hover */
	margin-left: 15px; /* Add some spacing */
}
.card {
	min-height: 80px;
}
.col {
	padding-top: 0;
	margin-top: 0;
}
.admin-section {
	border-bottom: 1px solid black; /* Add a 1-pixel solid border with a gray color below Admin */
	padding-bottom: 20px; /* Add spacing below the border for separation */
}
#eventCard {
	min-height: 80px;
	max-height: 80px;
}
.card-body {
	white-space: pre-wrap;
}
#button {
	display: flex;
	justify-content: flex-end;
	margin-top: 30px; /* Adjust the margin as needed */
}

#button button {
	/* Adjust the width of the button */
	min-width: 150px !important;
}
</style>
