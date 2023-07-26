import { createRouter, createWebHistory } from "vue-router"
import Home from "../components/Home.vue"
import CVEScan from "../components/CVEScan.vue"
import ServiceScan from "../components/ServiceScan.vue"
import PortScan from "../components/PortScan.vue"
import IPScan from "../components/IPScan.vue"
import DDOSAttack from "../components/DDOSAttack.vue"
import DOSAttack from "../components/DOSAttack.vue"

const routes = [
	{
		path: "/home",
		name: "Home",
		component: Home,
	},
	{
		path: "/cve",
		name: "CVEScan",
		component: CVEScan,
	},
	{
		path: "/service",
		name: "ServiceScan",
		component: ServiceScan,
	},
	{
		path: "/ip",
		name: "IPScan",
		component: IPScan,
	},
	{
		path: "/port",
		name: "PortScan",
		component: PortScan,
	},
	{
		path: "/dos",
		name: "DOSAttack",
		component: DOSAttack,
	},
	{
		path: "/ddos",
		name: "DDOSAttack",
		component: DDOSAttack,
	},
]

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
})

export default router
