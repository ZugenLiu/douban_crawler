# -*- coding:utf-8 -*-

import sys

sys.path.append("../")

import time
from threading import Thread

from apscheduler.schedulers.blocking import BlockingScheduler
from manager.ProxyManager import ProxyManager
from utils.utilFunction import validUsefulProxy

class ProxyRefreshSchedule(ProxyManager):

	def __init__(self):
		ProxyManager.__init__(self)

	def validProxy(self):
		"""
		Validate proxy in proxy pool
		"""
		exist_proxies = [p[0] for p in self.getProxiesUsage(0)]
		for proxy in exist_proxies:
			if not validUsefulProxy(proxy):
				self.useProxy(proxy)

def refreshPool():
	prs = ProxyRefreshSchedule()
	prs.validProxy()

def main(process_num=10):
	p = ProxyRefreshSchedule()

	#get new proxies
	p.refresh()

	pl = []
	for num in range(process_num):
		proc = Thread(target=refreshPool, args=())
		pl.append(proc)

	for num in range(process_num):
		pl[num].start()

	for num in range(process_num):
		pl[num].join()

def run():
    main()
    sched = BlockingScheduler()
    sched.add_job(main, 'interval', minutes=5)
    sched.start()


if __name__ == '__main__':
    run()