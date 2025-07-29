import QtQuick.Layouts 1.4
import QtQuick 2.12
import QtQuick.Controls 2.12 as Controls
import org.kde.kirigami 2.10 as Kirigami
import QtQuick.Window 2.3
import QtGraphicalEffects 1.0
import Mycroft 1.0 as Mycroft
import "." as Local

Mycroft.Delegate {
    id: rootSuggestionsView
    skillBackgroundSource: sessionData.bg_image ? sessionData.bg_image : "https://source.unsplash.com/1920x1080/?+music"
    property bool compactMode: parent.height >= 550 ? 0 : 1
    fillWidth: true
    leftPadding: 0
    rightPadding: 0
    topPadding: 0
    bottomPadding: 0

    onGuiEvent: {
        switch (eventName) {
            case "ocp.gui.show.suggestion.view.disambiguation":
                console.log("ocp.gui.show.suggestion.view.disambiguation")
                suggestionStackLayout.currentIndex = 1
                break
            case "ocp.gui.show.suggestion.view.playlist":
                console.log("ocp.gui.show.suggestion.view.playlist")
                suggestionStackLayout.currentIndex = 0
                break
        }
    }

    StackLayout {
        id: suggestionStackLayout
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom:  bottomBar.top
        anchors.bottomMargin: Mycroft.Units.gridUnit * 0.5
        anchors.margins: Mycroft.Units.gridUnit * 2
        currentIndex: 0

        Playlist {
            id: playlistView
            anchors.fill: parent
        }

        Disambiguation {
            id: disambiguationView
            anchors.fill: parent
        }
    }

    Rectangle {
        id: bottomBar
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: compactMode ? Mycroft.Units.gridUnit * 6 : Mycroft.Units.gridUnit * 4
        color: "transparent"
        visible: true
        enabled: true

        Kirigami.Separator {
            id: bottomBarSeparator
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            color: Kirigami.Theme.highlightColor
        }

        GridLayout {
            id: bottomBarLayout
            anchors.top: bottomBarSeparator.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: Mycroft.Units.gridUnit * 0.5
            columns: compactMode ? 1 : 2
            columnSpacing: Mycroft.Units.gridUnit * 0.5
            rowSpacing: Mycroft.Units.gridUnit * 0.5

            Rectangle {
                id: playlistButtonTangle
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: Kirigami.Theme.backgroundColor
                radius: 6

                Controls.Label {
                    id: playlistButtonLabel
                    anchors.centerIn: parent
                    text: "Playlist"
                    font.pixelSize: parent.height * 0.5
                    color: suggestionStackLayout.currentIndex == 0 ? Kirigami.Theme.highlightColor : Kirigami.Theme.textColor
                    elide: Text.ElideRight
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        suggestionStackLayout.currentIndex = 0
                    }
                    onPressed: {
                        playlistButtonTangle.color = Kirigami.Theme.highlightColor
                        playlistButtonLabel.color = Kirigami.Theme.backgroundColor
                    }
                    onReleased: {
                        playlistButtonTangle.color = Kirigami.Theme.backgroundColor
                        playlistButtonLabel.color = suggestionStackLayout.currentIndex == 0 ? Kirigami.Theme.highlightColor : Kirigami.Theme.textColor
                    }
                }
            }

            Rectangle {
                id: disambiguationViewButtonTangle
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: Kirigami.Theme.backgroundColor
                radius: 6

                Controls.Label {
                    id: disambiguationViewButtonLabel
                    anchors.centerIn: parent
                    text: "Search Results"
                    font.pixelSize: parent.height * 0.5
                    color: suggestionStackLayout.currentIndex == 1 ? Kirigami.Theme.highlightColor : Kirigami.Theme.textColor
                    elide: Text.ElideRight
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        suggestionStackLayout.currentIndex = 1
                    }
                    onPressed: {
                        disambiguationViewButtonTangle.color = Kirigami.Theme.highlightColor
                        disambiguationViewButtonLabel.color = Kirigami.Theme.backgroundColor
                    }
                    onReleased: {
                        disambiguationViewButtonTangle.color = Kirigami.Theme.backgroundColor
                        disambiguationViewButtonLabel.color = suggestionStackLayout.currentIndex == 1 ? Kirigami.Theme.highlightColor : Kirigami.Theme.textColor
                    }
                }
            }
        }
    }
}