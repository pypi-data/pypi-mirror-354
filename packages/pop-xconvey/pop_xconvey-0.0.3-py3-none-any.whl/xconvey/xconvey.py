import time
import platform
import paho.mqtt.client as mqtt
import threading

machine = platform.machine().lower()
if machine == "aarch64":
    product_file_path = "/etc/product"
else:
    product_file_path = "product"

class SensorBase:
    def __init__(self):
        self.__value = False
        self.__func = None 
        self.__param = None 
        self.__thread = None 
        self.__stop = False
        self.__repeat = 0

    def setVal(self, data):
        self.__value = data

    def read(self):
        return self.__value
    
    def __callback(self):
        while not self.__stop:
            if self.__param:
                self.__func(self.read(),self.__param)
            else:
                self.__func(self.read())
            time.sleep(self.__repeat/1000)

    def callback(self, func, repeat=1000,param=None):
        if not self.__thread:
            self.__func = func 
            self.__param = param
            self.__stop = False
            self.__thread = threading.Thread(target=self.__callback)
            self.__repeat = repeat
            self.__thread.start()

    def stop(self):
        if self.__thread:
            self.__stop = True
            self.__thread = None

class BlockBase:
    BLOCK = ""
    def __init__(self, device=None, timeout=3):
        self.TIMEOUT = timeout
        if device == None:
            try:
                with open(product_file_path) as file:
                    self.BROKER_DOMAIN = None
                    self.DEV_NUM = None
                    self.DEV_NAME = None
                    self.INSITUTION_NAME = None
                    for line in file:
                        line = line.strip()
                        if line.startswith('BROKER_DOMAIN='):
                            self.BROKER_DOMAIN = line.split('=')[1].strip()
                        if line.startswith('DEV_NUM='):
                            self.DEV_NUM = line.split('=')[1].strip()
                        if line.startswith('DEVICE_NAME='):
                            self.DEV_NAME = line.split('=')[1].strip()
                        if line.startswith('INSITUTION_NAME='):
                            self.INSITUTION_NAME = line.split('=')[1].strip()
                    if self.BROKER_DOMAIN is None:
                        raise "[Error] There is no product file. Please make sure the device has product info"
                self.TOPIC_HEADER = self.DEV_NAME+"/"+self.INSITUTION_NAME+self.DEV_NUM+"/"+self.BLOCK
            except FileNotFoundError:
                raise FileNotFoundError("Can't detect hbe device. Please set device argument.")
        self.value = None
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self.BROKER_DOMAIN)
        self._client.loop_start()

    def __del__(self):
        self._client.disconnect()

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._client.subscribe(self.topic+"/#")
    
    def _on_message(self, client, userdata, message):
        """
        Converting message
        """
        raise NotImplementedError

    @property
    def topic(self):
        return self.TOPIC_HEADER
    
class Safety(BlockBase):
    BLOCK="safety"

    class SWStart(SensorBase):
        pass

    class SWStop(SensorBase):
        pass

    def __init__(self):
        super().__init__()
        self.sw_start = self.SWStart()
        self.sw_stop = self.SWStop()

    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        if message.topic.find("sw_start") != -1:
            if payload == "active":
                self.sw_start.setVal(True)
            elif payload == "deactive":
                self.sw_start.setVal(False)
        elif message.topic.find("sw_stop") != -1:
            if payload == "stop":
                self.sw_stop.setVal(True)
            elif payload == "running":
                self.sw_stop.setVal(False)

    def indicator(self, color):
        if color not in ["red", "yellow", "green", "off"]:
            raise ValueError("Wrong value.")
        self._client.publish(self.topic+"/indicator", color, 0) 

class Transfer(BlockBase):
    BLOCK="transfer"
    
    class Encoder(SensorBase):
        pass

    def __init__(self):
        super().__init__()
        self.encoder = self.Encoder()
    
    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        if message.topic.find("encoder") != -1:
            self.encoder.setVal(int(payload))

    def run(self, step=1):
        if step > 10 or step < 0:
            raise ValueError("You did input wrong value.")
        self._client.publish(self.topic+"/motor/step", str(step), 0)
    
    def stop(self):
        self._client.publish(self.topic+"/motor/step", "0", 0)
        time.sleep(0.5)

class BlockServoBase(BlockBase):
    class Servo(SensorBase):
        pass

    class Photo(SensorBase):
        pass
    
    def __init__(self):
        super().__init__()
        self.servo = self.Servo()
        self.photo = self.Photo()

class Feeding(BlockServoBase):
    BLOCK = "feeding" 
    
    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        if message.topic.find("photo") != -1:
            if payload == "exist":
                self.photo.setVal(True)
            elif payload == "non-exist":
                self.photo.setVal(False) 
        elif message.topic.find("servo") != -1 and message.topic.find("state") != -1:
            if payload == "load" or payload == "supply":
                self.servo.setVal(payload)

    def load(self):
        self._client.publish(self.topic+"/servo/set", "load", 0)
    
    def supply(self):
        self._client.publish(self.topic+"/servo/set", "supply", 0)

    def toggle(self):
        if self.servo.read() == "load":
            self.supply()
        elif self.servo.read() == "supply":
            self.load()
    
class Processing(BlockServoBase):
    BLOCK = "processing"

    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        if message.topic.find("photo") != -1:
            if payload == "exist":
                self.photo.setVal(True)
            elif payload == "non-exist":
                self.photo.setVal(False) 
        elif message.topic.find("servo") != -1 and message.topic.find("state") != -1:
            if payload == "up" or payload == "down":
                self.servo.setVal(payload)

    def up(self):
        self._client.publish(self.topic+"/servo/set", "up", 0)

    def down(self):
        self._client.publish(self.topic+"/servo/set", "down", 0)
    
    def toggle(self):
        if self.servo.read() == "up":
            self.down()
        elif self.servo.read() == "down":
            self.up()

class Sorting(BlockServoBase):
    BLOCK = "sorting"

    class Inductive(SensorBase):
        pass

    class Line1Count(SensorBase):
        pass

    class Line2Count(SensorBase):
        pass

    def __init__(self):
        super().__init__()
        self.inductive = self.Inductive()
        self.line1count = self.Line1Count()
        self.line2count = self.Line2Count()

    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8")
        if message.topic.find("photo") != -1:
            if payload == "exist":
                self.photo.setVal(True)
            elif payload == "non-exist":
                self.photo.setVal(False) 
        elif message.topic.find("servo") != -1 and message.topic.find("state") != -1:
            if payload == "line1" or payload == "line2":
                self.servo.setVal(payload)
        elif message.topic.find("inductive") != -1:
            if payload == "metal":
                self.inductive.setVal(True)
            elif payload == "non-metal":
                self.inductive.setVal(False)
        elif message.topic.find("line1_count") != -1:
            self.line1count.setVal(self.line1count.read()+1)
        elif message.topic.find("line2_count") != -1:
            self.line2count.setVal(self.line2count.read()+1)

    def line1(self):
        self._client.publish(self.topic+"/servo/set", "line1", 0)

    def line2(self):
        self._client.publish(self.topic+"/servo/set", "line2", 0)
    
    def toggle(self):
        if self.servo.read() == "line1":
            self.line2()
        elif self.servo.read() == "line2":
            self.line1()