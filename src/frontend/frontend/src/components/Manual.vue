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
							<strong>[ STEP ]</strong> The user needs to provide the desired IP
							address of the targeted network and select either 'Vuln' or
							'Vulners' for the CVE Script field. Once all the necessary fields
							are filled, the user can begin the scan by clicking the “Run”
							button. During the scan, the system employs relevant nmap commands
							to detect vulnerabilities and exposures in the network.
						</p>
						<p>
							On the right side of the interface, there is an event log that
							provides real-time updates on the actions being executed by the
							system throughout the scan. Additionally, a status bar displays
							details such as the port, state, service, and associated CVE.
						</p>
					</li>
					<li>
						<strong>Service Scan</strong>
						<p>
							Service Scan should be able to scan a targeted network IP address
							and detect the various services in the network.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user needs to provide the desired IP
							address of the targeted network on which the user wants to perform
							the service scan, along with the scan type - TCP. After all fields
							are filled, the user can start the attack by clicking on the “Run”
							button.
						</p>
						<p>
							On the right side, there is an event log that will display in real
							time what is being done or executed by the system during the scan.
							Additionally, there is a status bar for the scan result to display
							the details of the result, such as the target IP address, port
							number, port name, product, extra information and version.
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
							<strong>[ STEP ]</strong> There will be 3 types of IP Scan which
							are Single IP, Multiple IP and IP Range. For the Single IP, the
							user needs to provide an IP address and subnet mask(Normally is
							24) of the targeted network on which the user wants to perform the
							IP scan, along with the scan type - TCP.
						</p>
						<p>
							For the Multiple IP, by clicking the 'add' button, the user needs
							to provide more than 1 IP address of the targeted network on which
							the user wants to perform the IP scan, along with the scan type -
							TCP.
						</p>
						<p>
							For the IP Range, by clicking the 'add' button, the user needs to
							provide a range IP address of the targeted network(eg.
							192.168.0.1-150) on which the user wants to perform the IP scan,
							along with the scan type - TCP.
						</p>
						<p>
							The user can start the scanning by clicking on the “Run” button.
							On the right side, there is an event log that will display in real
							time what is being done or executed by the system during the scan.
							Additionally, there is a status bar for the scan result to display
							a list of IP addresses of the host devices that are connected to
							the network.
						</p>
					</li>
					<li>
						<strong>Port Scan</strong>
						<p>
							Port Scan should be able to scan and display the open ports within
							the scanned network.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user needs to provide the desired IP
							address of the targeted network on which the user wants to perform
							the port scan, along with the scan type, either TCP or UDP. After
							all fields are filled, the user can start the attack by clicking
							on the “Run” button.
						</p>
						<p>
							On the right side, there is an event log that will display in real
							time what is being done or executed by the system during the scan.
							Additionally, there is a status bar for the scan result to display
							the details of the result, such as the port, status, protocol and
							host.
						</p>
					</li>
					<li>
						<strong>Denial-of-service (DoS) Attack</strong>
						<p>
							DoS Attack performs network attacks on the targeted network of the
							IP, which the user floods a targeted IP to prevent it from
							accessing connected online services and sites.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user need to provide the necessary
							information required for the DoS attack such as the targeted
							network IP address, target port, duration of the attack, type of
							attack - (SYN Flood, UDP Flood, ICMP Flood) and packet size. After
							all fields are filled, the user can start the attack by clicking
							on the “Run” button.
						</p>
						<p>
							On the right side, there is an event log that will display in real
							time what is being done or executed by the system during the
							attack. Additionally, there is a status tab for the current status
							of the attack to display the important information on the targeted
							network, such as bandwidth, latency, packet loss, throughput, and
							errors, which is being monitored as the attack is being performed.
						</p>
					</li>
					<li>
						<strong>Distributed Denial-of-Service (DDoS) Attack</strong>
						<p>
							DDoS attack is a DoS attack that performs network attacks by using
							multiple computers or machines to flood the targeted network of
							the IP to prevent it from accessing connected online services and
							sites.
						</p>
						<p>
							<strong>[ STEP ]</strong> The user needs to provide the necessary
							information required for the DoS attack such as the target network
							IP address, target port, duration of the attack, type of attacks -
							(SYN Flood, UDP Flood, ICMP Flood) and packet size. After all
							fields are filled, the user can start the attack by clicking on
							the “Run” button.
						</p>
						<p>
							On the right side, there is an event log that will display in real
							time what is being done or executed by the system during the
							attack. Additionally, there is a status tab for the current status
							of the attack to display the important information on the targeted
							network, such as bandwidth, latency, packet loss, throughput, and
							errors, which is being monitored as the attack is being performed.
						</p>
					</li>
					<li>
						<strong>Dashboard</strong>
						<p>
							The user can view the history log on the dashboard. There is a
							status tab that displays the history activities, and for more
							details of the history activities, the user can click on the
							activity. The details and results of the activity will be shown.
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
