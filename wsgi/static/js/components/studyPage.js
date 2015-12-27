var React = require('react');
var StudyAPI = require("../apis/studyApi");
var Util = require("../utils/util");
var ReactBootstrap = require('react-bootstrap');

var StatLabels = require('./statLabels');
var BadgeList = require('./badgeList');
var ClickableSpan = require('./clickableSpan');
var NewContentForm = require('./newContentForm');

var csrftoken = Util.getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!Util.csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var StudyPage = React.createClass({
    getInitialState: function() {
        return {
            'hanzis': [],
            'hanziIndex': 0,
            'unknowns': [],
            'knowns': [],
            'stats': {},
            'recapMode': false,
        };
    },
    
    addToKnowns: function() {
        this.updateProgress(true);
    },
    
    addToUnknowns: function() {
        this.updateProgress(false);
    },
    
    updateProgress: function(addToKnowns) {
        var oldState = this.state;
        if (addToKnowns) {
            oldState.knowns.push(this.state.hanzis[oldState.hanziIndex]);            
        } else {
            oldState.unknowns.push(this.state.hanzis[oldState.hanziIndex]);            
        }
        
        oldState.hanziIndex += 1;
        if (oldState.hanziIndex < this.state.hanzis.length) {
            this.setState(oldState);
        } else {
            if (!this.state.recapMode) {
                this.commitResult();
            }
            var hanzisToRecap = this.state.recapMode ? 
                Util.shuffle(this.state.hanzis):
                Util.shuffle(this.state.unknowns);
            oldState.hanziIndex = 0;
            oldState.unknowns = [];
            // recap
            this.recap(hanzisToRecap);
        }
    },

    commitResult: function() {
        var component = this;
        // commit to server
        var result = {
            "grasped_hanzi": this.state.knowns,
            "new_hanzi": this.state.unknowns
        };
        $.when(StudyAPI.updateLeitnerRecord(this.state.knowns, this.state.unknowns, this.props.category))
        .done(function() {
            component.refreshStat();
        });
    },

    recap: function(newHanzis) {
        console.log('recap:', newHanzis);

        this.setState({
            'hanzis': Util.shuffle(newHanzis),
            'recapMode': true,
            'hanziIndex': 0,
            'knowns': [],
            'unknowns': [],
        });
        this.refreshStat();
    },

    refreshStat: function() {
        var component = this;
        $.when(StudyAPI.getProgress(this.props.category))
        .done(function(progressResp) {
            component.setState({
                'stats': progressResp,
            });
        });
    },

    componentDidMount: function() {
        var component = this;
        $.when(StudyAPI.getLeitnerRecord(this.props.category), StudyAPI.getProgress(this.props.category))
        .done(function(leitnerRecordResp, progressResp){
            console.log(leitnerRecordResp);
            var hanzis = leitnerRecordResp[0].map(function(studyRecord) {
                    return studyRecord['hanzi']
                });
            component.setState({
                'hanzis': Util.shuffle(hanzis),
                'stats': progressResp[0]
            });
        });
    },
    
    getAddToRecapButton: function() {
        if (!this.state.recapMode) {
            return (<ReactBootstrap.Button bsStyle="info" onClick={this.addToUnknowns}>Add To Recap</ReactBootstrap.Button>);
        } else {
            return 'Recap mode';
        }
    },

    addNewContents: function(newContentArray, save) {
        if (save) {
            StudyAPI.updateLeitnerRecord([], newContentArray, this.props.category);
        }
        this.recap(newContentArray);
    },

    render: function() {
        console.log('StudyPage', this.props.category);
        var statLabels = <StatLabels stats={this.state.stats} />;
        
        const progressMax = this.state.hanzis.length;
        const progressNow = progressMax > 0 ? this.state.hanziIndex + 1 : 0;
        const hanziClass = this.props.category === "chinese_poem" ? "han_character_small" : "han_character";

        var hanzi = '';
        if (this.state.hanzis) {
            hanzi = this.state.hanzis[this.state.hanziIndex];
        }

        return (
            <div>
                <NewContentForm statLabels={statLabels} addNewContents={this.addNewContents} />
                <ReactBootstrap.ProgressBar max={progressMax} now={progressNow} bsStyle="success" label="%(now)s of %(max)s" />
                <ClickableSpan content={hanzi} clickHandler={this.addToKnowns} fontClass={hanziClass} />
                {this.getAddToRecapButton()}
                <BadgeList contents={this.state.unknowns} />
                <hr />
            </div>
        );
    }
});

module.exports = StudyPage;