import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "MQTT 客户端"

    Column {
        anchors.centerIn: parent
        spacing: 10

        // MQTT 服务器地址
        TextField {
            id: serverInput
            placeholderText: "MQTT 服务器地址"
        }

        // 连接按钮
        Button {
            text: "连接"
            onClicked: mqttClient.connectToServer(serverInput.text, 1883)
        }

        // 主题输入
        TextField {
            id: topicInput
            placeholderText: "主题"
        }

        // 消息内容输入
        TextField {
            id: messageInput
            placeholderText: "消息内容"
        }

        // 发布按钮
        Button {
            text: "发布消息"
            onClicked: mqttClient.publishMessage(topicInput.text, messageInput.text)
        }

        // 订阅按钮
        Button {
            text: "订阅主题"
            onClicked: mqttClient.subscribeTopic(topicInput.text)
        }

        // 日志显示区域
        TextArea {
            id: logArea
            readOnly: true
            height: 150
            width: parent.width
            placeholderText: "接收的消息将显示在这里"
        }
    }

    // 信号接收并显示消息
    Connections {
        target: mqttClient
        onMessageReceived: {
            logArea.text += "收到消息: 主题='" + topic + "', 内容='" + message + "'\n"
        }
    }
}
