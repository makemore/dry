import React from 'react';
import {
    Image,
    Platform,
    ScrollView,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    TextInput,
    Alert
} from 'react-native';
import {WebBrowser} from 'expo';

import axios from 'axios';

import {Button} from 'react-native';
import {ImagePicker} from 'expo';

import {MonoText} from '../components/StyledText';
import CommonDataManager from "../data/CommonDataManager";

export default class UploadScreen extends React.Component {
    static navigationOptions = {
        header: null,
    };

    state = {
        image: null,
        uploadProgress: 0
    };

    onNavigatorEvent(event) {
        console.log("tab selected", event.id);
        if (event.id === 'willAppear') {
            // Load data now
        }
    }

    constructor(props) {
        super(props);
        let commonData = CommonDataManager.getInstance();
        //his.setState({image: commonData.imageFileUri});
        //this.props.navigation.addListener(this.onNavigatorEvent);  //setOnNavigatorEvent(this.onNavigatorEvent.bind(this));
        //this.props.navigation.setOnNavigatorEvent(this.onNavigatorEvent.bind(this));
        this._handleTextChange = this._handleTextChange.bind(this);
        this._handleUpload = this._handleUpload.bind(this);

        var that = this;
        this.props.navigation.addListener("didFocus", function () {
            that.setState({image: commonData.imageFileUri});
            that.setState({audioFileUri: commonData.audioFileUri});
            //that.state.image = commonData.imageFileUri;
            //that.state.audioFileUri = commonData.audioFileUri;
        })
    }


    render() {
        let {image} = this.state;
        let commonData = CommonDataManager.getInstance();
        this.state.image = commonData.imageFileUri;
        this.state.audioFileUri = commonData.audioFileUri;
        this.state.text = '';


        return (!this.state.image || !this.state.audioFileUri ? (

            <View style={styles.centerView}>
                <Text style={styles.helpLinkText}>You need to Pap a snap and record some audio before you can
                    upload</Text>
            </View>

        ) : (
            <ScrollView style={styles.container}>
                <View style={styles.centerView}>
                    <View style={styles.buttonOuter}>
                        <TouchableOpacity onPress={this._handleUpload}>
                            <Text color="#fa2bf5" style={styles.buttonText2}>Upload</Text>
                        </TouchableOpacity>
                    </View>

                    <Text style={styles.buttonText3}>{this.state.uploadProgress}</Text>

                    <Text style={styles.buttonText3}>Add your poetry</Text>
                    <TextInput
                        style={styles.textAreaStuff}
                        onChangeText={this._handleTextChange}
                        value={this.state.text}
                        multiline={true}
                        underlineColorAndroid='transparent'
                    />
                </View>

                {/*{image && <Image source={{uri: image}} style={{width: 200, height: 200}}/>}
                    <View>
                        <Text>{this.state.audioFileUri}</Text>
                    </View>*/}

            </ScrollView>
        ));
    }

    _handleTextChange(incomingText) {
        this.state.text = incomingText;
    };

    _maybeRenderDevelopmentModeWarning() {
        if (__DEV__) {
            const learnMoreButton = (
                <Text onPress={this._handleLearnMorePress} style={styles.helpLinkText}>
                    Learn more
                </Text>
            );

            return (
                <Text style={styles.developmentModeText}>
                    Development mode is enabled, your app will be slower but you can use useful development
                    tools. {learnMoreButton}
                </Text>
            );
        } else {
            return (
                <Text style={styles.developmentModeText}>
                    You are not in development mode, your app will run at full speed.
                </Text>
            );
        }
    }

    _handleLearnMorePress = () => {
        WebBrowser.openBrowserAsync('https://docs.expo.io/versions/latest/guides/development-mode');
    };

    _handleHelpPress = () => {
        WebBrowser.openBrowserAsync(
            'https://docs.expo.io/versions/latest/guides/up-and-running.html#can-t-see-your-changes'
        );
    };

    _handleUpload = async () => {
        /*const {Location, Permissions} = Expo;
        const {status} = await Permissions.askAsync(Permissions.CAMERA_ROLL);
        const {status2} = await Permissions.askAsync(Permissions.CAMERA);

        let result = await ImagePicker.launchImageLibraryAsync({
            allowsEditing: false,
            //aspect: [4, 3],
        });

        console.log(result);

        if (!result.cancelled) {
            this.setState({image: result.uri});
        }
        else {
            throw new Error('Location permission not granted');
        }

        let localUri = result.uri;
        let filename = localUri.split('/').pop();

        // Infer the type of the image

        let type = match ? `image/${match[1]}` : `image`;

        // Upload the image using the fetch and FormData APIs

        // Assume "photo" is the name of the form field the server expects

        //let commonData = CommonDataManager.getInstance();
        //this.setState({image: result.uri});

        */

        let formData = new FormData();
        let commonData = CommonDataManager.getInstance();
        //let match = /\.(\w+)$/.exec(filename);

        //let type = match ? `image/${match[1]}` : `image`;
        var type = "image";

        var imageFilename = commonData.imageFileUri.replace(/^.*[\\\/]/, '');

        formData.append('image', {uri: commonData.imageFileUri, name: imageFilename, type});
        //var type = "audio";
        //commonData.setUserID("User1");
        //commonData.audioFileUri = info.uri;

        //var path = "file:///Users/chris/Library/Developer/CoreSimulator/Devices/9ED2720C-DB04-4CEC-B079-B2E0FB1D605E/data/Containers/Data/Application/50D353C7-8CEF-4C5B-B13E-0828B5BBD06D/Library/Caches/ExponentExperienceData/%2540chrisbarry%252Fdry/AV/recording-A8BBB717-44B0-468F-AC04-37BDA47F487E.caf";
        var path = commonData.audioFileUri;
        var audioFilename = path.replace(/^.*[\\\/]/, '');
        audioFilename = audioFilename.slice(0, -4);
        audioFilename += ".wav";
        type = "audio";
        formData.append('audio', {uri: path, name: audioFilename, type});
        formData.append('text', this.state.text);

        /*
         fetch("http://localhost:8000/social/spot-av-upload/", {
            //return await fetch("http://192.168.0.12:8000/social/spot-av-upload/", {
            //return await fetch("https://beta.drypoetry.life/social/spot-av-upload/", {
            method: 'POST',
            body: formData,
            header: {
                'content-type': 'multipart/form-data',
            },

        })
            .uploadProgress({interval: 100}, (written, total) => {
                console.log('uploaded', written / total)
            })
            .then(function () {
                Alert.alert(
                    'Upload complete',
                    "Keep up the papping and spot safe... ",
                    [
                        {text: 'OK', onPress: () => console.log('OK Pressed')},
                    ],
                    {cancelable: false}
                );
            }).catch((error) => {
                console.error(error);
                Alert.alert('Alert Title failure' + JSON.stringify(error))
            })
            .done();
            */

        var that = this;
        return await axios({
            method: 'post',
            url: "https://beta.drypoetry.life/social/spot-av-upload/",
            data: formData,
            onUploadProgress: function (progressEvent) {
                let percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                //console.debug('onUploadProgress called with', arguments, 'Percent Completed:' + percentCompleted)
                that.setState({uploadProgress: percentCompleted});
                //console.log(progressEvent);
            },
        }).then(function (response) {
            // handle success
            Alert.alert(
                'Upload complete',
                "Keep up the papping and spot safe... ",
                [
                    {
                        text: 'OK', onPress: function () {
                            console.log('OK Pressed');
                            that.setState({uploadProgress: 0});
                        }

                    },
                ],
                {cancelable: false}
            );
        })
            .catch(function (error) {
                // handle error
                //console.log(error);
                Alert.alert(error)
            });


    };
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        marginTop: 50
    },
    developmentModeText: {
        marginBottom: 20,
        color: 'rgba(0,0,0,0.4)',
        fontSize: 14,
        lineHeight: 19,
        textAlign: 'center',
    },
    centerView: {
        height: "100%",
        justifyContent: 'center',
        alignItems: 'center',
    },
    contentContainer: {
        paddingTop: 30,
        justifyContent: 'center',
        alignItems: 'center'
    },
    welcomeContainer: {
        alignItems: 'center',
        marginTop: 10,
        marginBottom: 20,
    },
    welcomeImage: {
        width: 100,
        height: 80,
        resizeMode: 'contain',
        marginTop: 3,
        marginLeft: -10,
    },
    getStartedContainer: {
        alignItems: 'center',
        marginHorizontal: 50,
    },
    homeScreenFilename: {
        marginVertical: 7,
    },
    codeHighlightText: {
        color: 'rgba(96,100,109, 0.8)',
    },
    codeHighlightContainer: {
        backgroundColor: 'rgba(0,0,0,0.05)',
        borderRadius: 3,
        paddingHorizontal: 4,
    },
    getStartedText: {
        fontSize: 17,
        color: 'rgba(96,100,109, 1)',
        lineHeight: 24,
        textAlign: 'center',
    },
    tabBarInfoContainer: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        ...Platform.select({
            ios: {
                shadowColor: 'black',
                shadowOffset: {height: -3},
                shadowOpacity: 0.1,
                shadowRadius: 3,
            },
            android: {
                elevation: 20,
            },
        }),
        alignItems: 'center',
        backgroundColor: '#fbfbfb',
        paddingVertical: 20,
    },
    tabBarInfoText: {
        fontSize: 17,
        color: 'rgba(96,100,109, 1)',
        textAlign: 'center',
    },
    navigationFilename: {
        marginTop: 5,
    },
    helpContainer: {
        marginTop: 15,
        alignItems: 'center',
    },
    helpLink: {
        paddingVertical: 15,
    },
    helpLinkText: {
        fontSize: 20,
        color: '#3cc3f3',
        textAlign: "center"
    },
    buttonOuter: {
        marginRight: 40,
        marginLeft: 40,
        marginTop: 10,
        paddingTop: 10,
        paddingBottom: 10,
        backgroundColor: '#555555',
        borderRadius: 10,
        width: "80%",
        borderWidth: 1,
        borderColor: '#fff'
    },
    buttonText1: {
        color: '#3cc3f3',
        textAlign: 'center',
        paddingLeft: 10,
        paddingRight: 10
    },
    buttonText2: {
        color: '#fa2bf5',
        textAlign: 'center',
        paddingLeft: 10,
        paddingRight: 10
    },
    buttonText3: {
        color: '#fa2bf5',
        textAlign: 'center',
        paddingTop: 30,
        paddingBottom: 30,
        paddingLeft: 10,
        paddingRight: 10
    },
    textAreaStuff: {
        height: 150,
        marginLeft: 10,
        marginRight: 10,
        borderColor: 'gray',
        borderWidth: 1,
        "width": "80%",
        marginBottom:300
    },
    loaderBar: {
        width: "50%",
        backgroundColor: "#000000",
        height: 10,
    }
});
