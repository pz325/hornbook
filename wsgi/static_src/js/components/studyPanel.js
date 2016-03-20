"use strict";

var React = require('react');
var ReactBootstrap = require('react-bootstrap');

var StatLabels = require('./statLabels');
var BadgeList = require('./badgeList');
var ClickableSpan = require('./clickableSpan');
var NewContentForm = require('./newContentForm');


var StudyPanel = React.createClass({
    propTypes: {
        hanzis: React.PropTypes.array.isRequired,
        stats: React.PropTypes.shape({
            new: React.PropTypes.number,
            studying: React.PropTypes.number,
            grasped: React.PropTypes.number
        }).isRequired,
        sessionDoneHandler: React.PropTypes.func.isRequired,
        newContentAddedHandler: React.PropTypes.func.isRequired,
        recapMode: React.PropTypes.bool,        // default false
        fontClass: React.PropTypes.string
    },

    getInitialState: function() {
        return {
            'hanziIndex': 0,
            'unknowns': [],
            'knowns': [],
        };
    },
    
    addToKnowns: function() {
        console.log('StudyPanel::addToKnowns()');
        this.updateProgress(true);
    },
    
    addToUnknowns: function() {
        console.log('StudyPanel::addToUnknowns()');
        this.updateProgress(false);
    },
    
    updateProgress: function(addToKnowns) {
        var oldState = this.state;
        if (addToKnowns) {
            oldState.knowns.push(this.props.hanzis[oldState.hanziIndex]);            
        } else {
            oldState.unknowns.push(this.props.hanzis[oldState.hanziIndex]);            
        }
        
        oldState.hanziIndex += 1;

        console.log('StudyPanel::updateProgress() addtoknows: ', addToKnowns, 
            'knowns: ', oldState.knowns,
            'unknowns: ', oldState.unknowns,
            'hanziIndex:', oldState.hanziIndex);

        if (oldState.hanziIndex < this.props.hanzis.length) {
            this.setState(oldState);
        } else {
            this.props.sessionDoneHandler(oldState.knowns, oldState.unknowns);
            this.setState(this.getInitialState());
        }
    },
    
    getAddToRecapButton: function() {
        if (!this.props.recapMode) {
            return (<ReactBootstrap.Button ref='StudyPanel_buttonAddToUnknown' bsStyle="info" onClick={this.addToUnknowns}>Add To Recap</ReactBootstrap.Button>);
        } else {
            return 'Recap mode';
        }
    },

    addNewContents: function(newContentArray, save) {
        this.props.newContentAddedHandler(newContentArray, save);
    },

    render: function() {
        // var statLabels = <StatLabels stats={this.props.stats} />;
        
        var progressMax = this.props.hanzis.length;
        var progressNow = progressMax > 0 ? this.state.hanziIndex + 1 : 0;
        var fontClass = this.props.fontClass ? this.props.fontClass : 'han_character';
        var hanzi = this.props.hanzis ? this.props.hanzis[this.state.hanziIndex] : '';

        return (
            <div>
                <NewContentForm ref='StudyPanel_newContentForm' addNewContents={this.addNewContents} />
                <StatLabels stats={this.props.stats} />
                <ReactBootstrap.ProgressBar ref='StudyPanel_progressBar' max={progressMax} now={progressNow} bsStyle="success" label="%(now)s of %(max)s" />
                <ClickableSpan ref='StudyPanel_clickableSpan' content={hanzi} clickHandler={this.addToKnowns} fontClass={fontClass} />
                {this.getAddToRecapButton()}
                <BadgeList ref='StudyPanel_badgeList' contents={this.state.unknowns} />
                <hr />
            </div>
        );
    }
});

module.exports = StudyPanel;