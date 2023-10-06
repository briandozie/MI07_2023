import { createRouter, createWebHistory } from "vue-router"
import Login from "../components/Login.vue"
import Home from "../components/Home.vue"
import CVEScan from "../components/CVEScan.vue"
import ServiceScan from "../components/ServiceScan.vue"
import PortScan from "../components/PortScan.vue"
import IPScan from "../components/IPScan.vue"
import DDOSAttack from "../components/DDOSAttack.vue"
import DOSAttack from "../components/DOSAttack.vue"
import Dashboard from "../components/Dashboard.vue"
import HistoryDetail from "../components/HistoryDetail.vue"
import Manual from "../components/Manual.vue"
import axios from "axios"

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
	{
		path: "/dashboard",
		name: "DASHBOARD",
		meta: { title: "Dashboard" },
		component: Dashboard,
	},
	{
		path: "/history/:id", // Use a dynamic route parameter to pass the row id
		name: "historyDetail",
		meta: { title: "History Details" },
		component: HistoryDetail,
	},
	{
		path: "/manual",
		name: "Manual",
		meta: { title: "Manual" },
		component: Manual,
	},
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
})

router.beforeEach(async (to, from, next) => {
	// Check if the user is navigating to the login page
	if (to.name == "Login" && from.path == "/") {
		alert("Wrong route!")
		document.title = to.meta.title
		next()
	} else if (to.name === "Login" && from.path !== "/") {
		// Logouts the user and removes HTTP-only cookies
		alert("In Router Guard!")
		try {
			const loggedOut = await logout()
			console.log(loggedOut)
			if (loggedOut) {
				axios.defaults.headers.common["Authorization"] = ""
				next()
			} else {
				console.error("Something went wrong!")
			}
		} catch (error) {
			console.error("Something happened during logout!")
		}
	} else {
		try {
			// Checks to see if user is authenticated or not
			const isAuthenticated = await checkAuthenticationStatus()
			console.log(isAuthenticated)
			// If user is not authenticated, redirect to login page
			if (!isAuthenticated) {
				next({ name: "Login" })
			} else {
				document.title = to.meta.title
				next()
			}
		} catch (error) {
			console.error("An error occurred during authentication check:", error)
			next({ name: "Login" }) // Redirect to login page in case of error
		}
	}
})

async function checkAuthenticationStatus() {
	return new Promise((resolve, reject) => {
		axios
			.get("http://localhost:5000/check-auth/")
			.then((res) => {
				console.log(res.data)
				if (res.status == 201) {
					// Return true if authorised
					resolve(true)
				} else {
					resolve(false)
				}
			})
			.catch((error) => {
				if (error.response.status == 401) {
					console.log("User is unauthenticated.")
					resolve(false)
				} else {
					console.log("An error occured.")
					reject(error)
				}
			})
	})
}

function logout() {
	return new Promise((resolve, reject) => {
		axios
			.post("http://localhost:5000/check-auth/logout")
			.then((res) => {
				console.log(res.data)
				resolve(true) // Resolve the promise if the logout is successful
			})
			.catch((error) => {
				console.error("An error occurred during logout:", error)
				reject(error) // Reject the promise if there's an error during logout
			})
	})
}

export default router
