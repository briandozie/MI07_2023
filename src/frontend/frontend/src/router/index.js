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
		meta: { title: "SDN Intrusion & Penetration System" },
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
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
})

router.beforeEach((to, from, next) => {
	document.title = to.meta.title
	next()
})

export default router
