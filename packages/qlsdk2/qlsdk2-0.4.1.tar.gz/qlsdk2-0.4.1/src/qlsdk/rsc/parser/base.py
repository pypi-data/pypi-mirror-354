from qlsdk.rsc.interface import IDevice, IParser

from loguru import logger
from threading import Thread
from time import time_ns
from qlsdk.rsc.command import CommandFactory

class TcpMessageParser(IParser):
    def __init__(self, device : IDevice):
        # 待解析的数据来源于该设备
        self.device = device    
        self.running = False
        
        self.cache = b''
        
    @property
    def header(self):
        return b'\x5A\xA5'
    
    @property
    def header_len(self):
        return 14
    
    @property
    def cmd_pos(self):
        return 12
        
    def append(self, buffer):
        self.cache += buffer
        logger.debug(f"已缓存的数据长度: {len(self.cache)}")
        
    def __parser__(self):
        logger.info("数据解析开始")
        while self.running:
            if len(self.cache) < 14:
                continue
            if self.cache[0] != 0x5A or self.cache[1] != 0xA5:
                self.cache = self.cache[1:]
                continue
            pkg_len = int.from_bytes(self.cache[8:12], 'little')
            logger.trace(f" cache len: {len(self.cache)}, pkg_len len: {len(self.cache)}")
            # 一次取整包数据
            if len(self.cache) < pkg_len:
                continue
            pkg = self.cache[:pkg_len]
            self.cache = self.cache[pkg_len:]
            self.unpack(pkg)
    
    def unpack(self, packet):        
        # 提取指令码
        cmd_code = int.from_bytes(packet[self.cmd_pos : self.cmd_pos + 2], 'little')
        cmd_class = CommandFactory.create_command(cmd_code)
        logger.debug(f"收到指令：{cmd_class.cmd_desc}[{hex(cmd_code)}]")
        instance = cmd_class(self.device)
        start = time_ns()
        logger.debug(f"开始解析: {start}")
        instance.parse_body(packet[self.header_len:-2])
        logger.debug(f"解析完成:{time_ns()}, 解析耗时：{time_ns() - start}ns")
        return instance
            
    def start(self):
        self.running = True
        parser = Thread(target=self.__parser__,)
        parser.daemon = True
        parser.start()
        