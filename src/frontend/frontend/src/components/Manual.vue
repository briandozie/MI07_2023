<template>
	<div>
		<!-- Primary Navigation Bar -->
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

		<!-- Secondary Navigation Bar -->
		<nav class="navbar bg-secondary" data-bs-theme="dark">
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

		<div id="content" class="container">
			<h1>Information and Guidance</h1>
			<div id="manualContent">
				<ul>
					<li>
						<strong>Common Vulnerabilities and Exposures (CVE) Scan</strong>
						<p>
							CVE Scan should be able to scan a targeted network and identify
							the potential threats and vulnerabilities present in the network.
						</p>
						<p>
							<strong>[ STEP ]</strong> User is able to enter the desired IP
							address of the targeted network that the user wants to perform the
							vulnerability scan. For the CVE Script field, user can select
							either 'Vuln' or 'Vulners'. After all field are filled, the user
							can start the attack by clicking on the “Run” button. The system
							uses relevant nmap commands and performs a network scan on the
							targeted network to detect all the common vulnerabilities and
							exposures present in the network.
						</p>
						<p>
							There is an event log that will display in realtime what is being
							done or executed by the system during the scan. Additionally, on
							the right side of the webpage, there is a status tab that will
							display the result of the scan. This section will display the
							details of the result such as the target IP address, number of
							ports scanned, and the list of vulnerabilities of each port.
						</p>
					</li>
					<li>
						<strong>Service Scan</strong>
						<p>
							Service Scan should be able to scan a targeted network IP address
							and detect the various services in the network.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user is able to enter the desired IP
							address and subnet mask of the targeted network that the user
							wants to perform the Service scan, along with the scan type - TCP.
							After all field are filled, the user can start the attack by
							clicking on the “Run” button.
						</p>
						<p>
							At the bottom of the webpage, there is an event log that will
							display in realtime what is being done or executed by the system
							during the scan. Additionally, on the right side of the webpage,
							there is a status tab that will display the result of the scan.
							This section will display the details of the result such as the
							target IP address, number of Ports scanned, and the list of active
							services running on the ports.
						</p>
					</li>
					<li>
						<strong>IP Scan</strong>
						<p>
							IP Scan should be able to scan a targeted network and find out the
							IP addresses of the host devices that are connected to the
							network.
						</p>
						<p>
							<strong>[ STEP ]</strong> There will be 3 type of IP Scan which
							are Single IP, Multiple IP and IP Range. For the Single IP,The
							user is able to enter a IP address and subnet mask(Normally is 24)
							of the targeted network that the user wants to perform the IP
							scan, along with the scan type - TCP.
						</p>
						<p>
							For the Multiple IP, by clicking the 'add' button, the user is
							able to enter more than 1 IP address of the targeted network that
							the user wants to perform the IP scan, along with the scan type -
							TCP.
						</p>
						<p>
							For the IP Range, by clicking the 'add' button, the user is able
							to enter a range IP address of the targeted network(eg.
							192.168.0.1-150) that the user wants to perform the IP scan, along
							with the scan type - TCP.
						</p>
						<p>
							The user can start the attack by clicking on the “Run” button.At
							the bottom of the webpage, there is an event log that will display
							in realtime what is being done or executed by the system during
							the scan. Additionally, on the right side of the webpage, there is
							a status tab that will display the result of the scan. This
							section will display the details of the result such as the target
							IP address, number of IPs scanned, and the list of active IP
							addresses.
						</p>
					</li>
					<li>
						<strong>Port Scan</strong>
						<p>
							Port Scan should be able to scan and display the open ports within
							the scanned network.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user is able to enter the desired IP
							address and subnet mask of the targeted network that the user
							wants to perform the port scan, along with the scan type, either
							TCP or UDP. After all field are filled, the user can start the
							attack by clicking on the “Run” button.
						</p>
						<p>
							At the bottom of the webpage, there is an event log that will
							display in realtime what is being done or executed by the system
							during the scan. Additionally, on the right side of the webpage,
							there is a status tab that will display the result of the scan.
							This section will display the details of the result such as the
							target IP address, number of ports scanned, open ports detected,
							and the list of open ports.
						</p>
					</li>
					<li>
						<strong>Denial-of-service (DoS) Attack</strong>
						<p>
							DoS Attack should perform network attacks on the targeted network.
							The network attacks performed should simulate real-world network
							intrusions and scenarios.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user is able to enter the necessary
							information required for the DoS attack such as the target network
							IP address, duration of attack, and type of attack - SYN Flood.
							After all field are filled, the user can start the attack by
							clicking on the “Run” button.
						</p>
						<p>
							At the bottom of the webpage, there is an event log that will
							display in realtime what is being done or executed by the system
							during the attack. Next, on the right side of the webpage, there
							is a status tab that will display the current status of the
							attack. This section will display the important information on the
							targeted network such as bandwidth, latency, packet loss,
							throughput, and errors, which is being monitored as the attack is
							being performed.
						</p>
					</li>
					<li>
						<strong>Distributed Denial-of-Service (DDoS) Attack</strong>
						<p>
							DDoS Attack should perform network attacks on the targeted
							network. The network attacks performed should simulate real-world
							network intrusions and scenarios.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user is able to enter the necessary
							information required for the DDoS attack such as the target
							network IP address, duration of attack, and type of attack - SYN
							Flood. After all field are filled, the user can start the attack
							by clicking on the “Run” button.
						</p>
						<p>
							At the bottom of the webpage, there is an event log that will
							display in realtime what is being done or executed by the system
							during the attack. Next, on the right side of the webpage, there
							is a status tab that will display the current status of the
							attack. This section will display the important information on the
							targeted network such as bandwidth, latency, packet loss,
							throughput, and errors, which is being monitored as the attack is
							being performed.
						</p>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>

<script></script>

<style scoped>
.navbar {
	height: 50px;
}

ul {
	padding: 0;
}

li {
	margin-bottom: 20px;
}

li strong {
	font-size: 18px;
}

li p {
	margin-bottom: 0px;
}
#content {
	padding-top: 50px;
}
#manualContent {
	padding-top: 20px;
}
</style>
