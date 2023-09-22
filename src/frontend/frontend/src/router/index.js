import { createRouter, createWebHistory } from "vue-router"
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

const routes = [
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

router.beforeEach((to, from, next) => {
	document.title = to.meta.title
	next()
})

export default router
