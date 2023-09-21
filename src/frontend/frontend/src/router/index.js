import { createRouter, createWebHistory } from "vue-router"
import Login from "../components/Login.vue"
import Home from "../components/Home.vue"
import CVEScan from "../components/CVEScan.vue"
import ServiceScan from "../components/ServiceScan.vue"
import PortScan from "../components/PortScan.vue"
import IPScan from "../components/IPScan.vue"
import DDOSAttack from "../components/DDOSAttack.vue"
import DOSAttack from "../components/DOSAttack.vue"

const routes = [
	{
		path: "/",
		redirect: "/login", // Redirect default path to login page
	},
	{
		path: "/login",
		name: "Login",
		meta: { title: "Login" },
		component: Login,
		beforeEnter: (to, from, next) => {
			if (from.path !== "/") {
				alert("You have been logged out")

				// Removes the user token from localStorage upon logout
				removeAuthToken()
			}
			next()
		},
	},
	{
		path: "/home",
		name: "Home",
		meta: { title: "SDN Intrusion & Penetration System" },
		component: Home,
	},
	{
		path: "/cve",
		name: "CVEScan",
		meta: { title: "CVE Scan" },
		component: CVEScan,
	},
	{
		path: "/service",
		name: "ServiceScan",
		meta: { title: "Service Scan" },
		component: ServiceScan,
	},
	{
		path: "/ip",
		name: "IPScan",
		meta: { title: "IP Scan" },
		component: IPScan,
	},
	{
		path: "/port",
		name: "PortScan",
		meta: { title: "Port Scan" },
		component: PortScan,
	},
	{
		path: "/dos",
		name: "DOSAttack",
		meta: { title: "DoS Attack" },
		component: DOSAttack,
	},
	{
		path: "/ddos",
		name: "DDOSAttack",
		meta: { title: "DDoS Attack" },
		component: DDOSAttack,
	},
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
})

router.beforeEach((to, from, next) => {
	// Checks to see if user is authenticated or not
	const isAuthenticated = checkAuthenticationStatus()
	// If user is unauthenticated, redirect to login page
	if (to.name !== "Login" && !isAuthenticated) {
		next({ name: "Login" })
	} else {
		document.title = to.meta.title
		next()
	}
})

function checkAuthenticationStatus() {
	// Retrive token from localStorage
	const authToken = localStorage.getItem("authToken")

	//Checks to see if authToken is valid
	const isAuthenticated = !!authToken
	return isAuthenticated
}

function removeAuthToken() {
	//Removes user token from localStorage
	localStorage.removeItem("authToken")
}

export default router
