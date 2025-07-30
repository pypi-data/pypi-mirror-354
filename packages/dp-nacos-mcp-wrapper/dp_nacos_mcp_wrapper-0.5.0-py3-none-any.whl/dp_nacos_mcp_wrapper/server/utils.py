import asyncio
import socket
import threading
from enum import Enum
import ipaddress
import logging

import jsonref
import psutil

logger = logging.getLogger(__name__)

def get_first_non_loopback_ip():
	"""
	获取第一个非回环地址的IP，优先选择最合适的网络接口
	
	优先级顺序：
	1. 公网IP地址
	2. 私有网络IP地址（按照常用性排序）
	3. 排除虚拟网络接口和Docker接口
	"""
	try:
		preferred_ips = []
		fallback_ips = []
		
		# 获取网络接口状态
		net_stats = psutil.net_if_stats()
		
		for interface, addrs in psutil.net_if_addrs().items():
			# 跳过未激活的网络接口
			if interface in net_stats and not net_stats[interface].isup:
				continue
				
			# 跳过明显的虚拟网络接口
			if _is_virtual_interface(interface):
				continue
			
			for addr in addrs:
				if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
					try:
						ip = ipaddress.IPv4Address(addr.address)
						
						# 公网IP地址优先级最高
						if ip.is_global:
							preferred_ips.append((1, addr.address, interface))
						# 私有网络IP地址
						elif ip.is_private:
							priority = _get_private_ip_priority(addr.address)
							preferred_ips.append((priority, addr.address, interface))
						# 其他IP地址作为备选
						else:
							fallback_ips.append((10, addr.address, interface))
					except ipaddress.AddressValueError:
						logger.warning(f"Invalid IP address: {addr.address}")
						continue
		
		# 合并并排序IP地址列表
		all_ips = preferred_ips + fallback_ips
		if all_ips:
			# 按优先级排序，返回最佳IP
			all_ips.sort(key=lambda x: x[0])
			selected_ip = all_ips[0][1]
			selected_interface = all_ips[0][2]
			logger.info(f"Selected IP address: {selected_ip} from interface: {selected_interface}")
			return selected_ip
		
		logger.warning("No suitable IP address found")
		return None
		
	except Exception as e:
		logger.error(f"Error getting IP address: {e}")
		return None

def _is_virtual_interface(interface_name: str) -> bool:
	"""
	判断是否为虚拟网络接口
	"""
	virtual_prefixes = [
		'docker', 'br-', 'veth', 'virbr', 'vmnet', 'vbox',
		'tap', 'tun', 'lo', 'dummy', 'bond', 'team'
	]
	
	interface_lower = interface_name.lower()
	return any(interface_lower.startswith(prefix) for prefix in virtual_prefixes)

def _get_private_ip_priority(ip_address: str) -> int:
	"""
	为私有IP地址分配优先级
	
	优先级顺序：
	2: 192.168.x.x (最常用的家庭/办公网络)
	3: 10.x.x.x (企业网络)
	4: 172.16.x.x - 172.31.x.x (Docker默认网络范围)
	"""
	try:
		ip = ipaddress.IPv4Address(ip_address)
		
		# 192.168.x.x 网段 (最常用)
		if ip in ipaddress.IPv4Network('192.168.0.0/16'):
			return 2
		# 10.x.x.x 网段
		elif ip in ipaddress.IPv4Network('10.0.0.0/8'):
			return 3
		# 172.16.x.x - 172.31.x.x 网段
		elif ip in ipaddress.IPv4Network('172.16.0.0/12'):
			return 4
		else:
			return 5
	except ipaddress.AddressValueError:
		return 9

def jsonref_default(obj):
	if isinstance(obj, jsonref.JsonRef):
		return obj.__subject__
	raise TypeError(
			f"Object of type {obj.__class__.__name__} is not JSON serializable")

class ConfigSuffix(Enum):
	TOOLS = "-mcp-tools.json"
	PROMPTS = "-mcp-prompt.json"
	RESOURCES = "-mcp-resource.json"
	MCP_SERVER = "-mcp-server.json"