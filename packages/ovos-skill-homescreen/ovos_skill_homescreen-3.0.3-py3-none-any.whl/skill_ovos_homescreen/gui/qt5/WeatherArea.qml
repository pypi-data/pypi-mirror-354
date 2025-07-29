import QtQuick.Layouts 1.4
import QtQuick 2.9
import QtQuick.Controls 2.12
import org.kde.kirigami 2.11 as Kirigami
import QtGraphicalEffects 1.0
import Mycroft 1.0 as Mycroft

Rectangle {
    color: "transparent"
    id: weatherItemBox
    property bool verticalMode: false

    RowLayout {
        anchors.fill: parent
        anchors.margins: Mycroft.Units.gridUnit / 2

        Rectangle {
            Layout.preferredWidth: offlineModeIconLayerOne.implicitWidth + Mycroft.Units.gridUnit * 3
            Layout.fillHeight: true
            Layout.alignment: weatherItemBox.verticalMode ? Qt.AlignHCenter : Qt.AlignRight
            color: "transparent"
            visible: idleRoot.systemConnectivity == "offline" || idleRoot.systemConnectivity == "network" ? 1 : 0

            Kirigami.Icon {
                id: offlineModeIconLayerOne
                width: parent.height * 0.80
                height: width
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                visible: true
                source: switch(idleRoot.systemConnectivity) {
                    case "offline":
                        return Qt.resolvedUrl("icons/offline_layer_one.svg");
                        break;
                    case "network":
                        return Qt.resolvedUrl("icons/no-internet.svg");
                        break;
                }

                ColorOverlay {
                    anchors.fill: offlineModeIconLayerOne
                    source: offlineModeIconLayerOne
                    color: Kirigami.Theme.textColor
                }
            }

            Kirigami.Icon {
                id: offlineModeIconLayerTwo
                width: parent.height * 0.80
                height: width
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                visible: true
                source: Qt.resolvedUrl("icons/offline_layer_two.svg")

                ColorOverlay {
                    anchors.fill: offlineModeIconLayerTwo
                    source: offlineModeIconLayerTwo
                    color: Kirigami.Theme.highlightColor
                }
            }
        }

        Rectangle {
            color: "transparent"
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: idleRoot.weatherEnabled
            enabled: idleRoot.weatherEnabled

            Kirigami.Icon {
                id: weatherItemIcon
                source: Qt.resolvedUrl(getWeatherImagery(sessionData.weather_code))
                width: parent.height * 0.90
                height: width
                anchors.right: parent.right
                anchors.rightMargin: weatherItemBox.verticalMode ? Mycroft.Units.gridUnit / 2 : 0
                anchors.verticalCenter: parent.verticalCenter
                visible: true
                layer.enabled: true
                layer.effect: DropShadow {
                    verticalOffset: 4
                    color: idleRoot.shadowColor
                    radius: 11
                    spread: 0.4
                    samples: 16
                }
            }
        }

        Rectangle {
            color: "transparent"
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: idleRoot.weatherEnabled
            enabled: idleRoot.weatherEnabled

            Text {
                id: weatherItem
                text: sessionData.weather_temp + "°"
                width: parent.width
                height: parent.height
                fontSizeMode: Text.Fit
                minimumPixelSize: parent.height / 2
                maximumLineCount: 1
                font.pixelSize: parent.height
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: weatherItemBox.verticalMode ? Text.AlignLeft : Text.AlignHCenter
                color: "white"
                visible: true
                layer.enabled: true
                layer.effect: DropShadow {
                    verticalOffset: 4
                    color: idleRoot.shadowColor
                    radius: 11
                    spread: 0.4
                    samples: 16
                }
            }
        }
    }
}
