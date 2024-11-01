# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtMqtt import QMQTTClient

class MQTTClient(QObject):
    messageReceived = Signal(str, str) # 信号：用于发送主题和消息内容到QML

    def __init__(self):
        super().__init__()
        self.client = QMQTTClient()
        self.client.connected.connect(self.on_connect)
        self.client.disconnected.connect(self.on_disconnect)
        self.client.messageReceived.connect(self.on_message_recevied)

    @Slot(str, int)
    def connectToServer(self, hostname, port):
        self.client.setHostname(hostname)
        self.client.setPort(port)
        self.client.connectToHost()

    @Slot()
    def disconnectFromServer(self):
        self.client.disconnectFromHost()

    @Slot(str, str)
    def publishMessage(self, topic, message):
        if topic and message:
            self.client.publish(topic, message.encode('utf-8'))

    @Slot(str)
    def subscribeTopic(self, topic):
        if topic:
            self.client.subscribe(topic)

    def on_connect(self):
        print("连接成功")

    def on_disconnect(self):
        print("断开连接")

    def on_message_received(self, message, topic):
        msg = message.data().decode("utf-8")
        self.messageReceived.emit(topic, msg)  # 将消息发送到 QML 界面


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # 创建MQTT客户端并绑定到QML
    mqtt_client = MQTTClient()
    engine.rootContext().setContextProperty("mqttClient", mqtt_client)


    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

