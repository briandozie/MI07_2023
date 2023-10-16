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

		<p>This is the Home Page</p>
		<!-- <button type="button" class="btn btn-primary">{{ msg }}</button> -->
	</div>
</template>

<script>
// import axios from "axios"
// export default {
//   name: "Home",
//   data() {
//     return {
//       msg: "",
//     }
//   },
//   methods: {
//     getResponse() {
//       const path = "http://localhost:5000/home"
//       axios
//         .get(path)
//         .then((res) => {
//           console.log(res.data)
//           this.msg = res.data
//         })
//         .catch((err) => {
//           console.log(err)
//         })
//     },
//   },
//   created() {
//     this.getResponse()
//   },
// }
</script>

<style>
#cm-logo {
	padding-right: 15px;
}
#primaryNav {
	height: 80px;
}
p {
	display: block;
	padding-top: 10px;
	margin-left: 15px;
}
.navbar-brand.ms-auto {
	color: #fff; /* Text color */
	text-decoration: none; /* Remove underline */
	cursor: pointer; /* Change cursor on hover */
	margin-left: 15px; /* Add some spacing */
}
</style>
