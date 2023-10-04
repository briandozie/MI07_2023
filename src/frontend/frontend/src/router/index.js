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
	if (to.name == "Login") {
		document.title = to.meta.title
		next()
	} else {
		try {
			// Checks to see if user is authenticated or not
			const isAuthenticated = await checkAuthenticationStatus()
			console.log(isAuthenticated)
			// If user is unauthenticated, redirect to login page
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
					console.log("In res.status == 201")
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

function removeAuthToken() {
	//Removes user token from localStorage
	localStorage.removeItem("token")
}

export default router
