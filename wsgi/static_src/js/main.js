var React = require('react');
var ReactDOM = require('react-dom');

var HornbookNavBar = require('./components/hornbookNavBar');
var StudyPanel = require('./components/studyPanel');
var StudyAPI = require('./apis/studyApi');
var Util = require("./utils/util");

var csrftoken = Util.getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!Util.csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var username = $("#app").attr("data-username");
var categories = [{'category': 'read_hanzi', 'display': '认字'},
        {'category': 'write_hanzi', 'display': '写字'},
        {'category': 'chinese_poem', 'display': '古诗'}
    ];

var App = React.createClass({
    getInitialState: function() {
        return {
            'hanzis': [],
            'stats': {},
            'category': 'read_hanzi',
            'recapMode': false,
            'fontClass': 'han_character'
        };
    },

    studyCategory: function(category) {
        this._initStudyPanel(category);
    },

    studyPanelSessionDoneHandler: function(knowns, unknowns) {
        console.log('App::studyPanelSessionDoneHandler(), knowns: ', knowns, ' unknowns: ', unknowns);
        if (this.state.recapMode) {
            // recap mode, reset study panel with shuffled knowns
            this._shuffleStudyPanel(knowns);
        }
        else {
            // ajax post knowns and unknowns
            this._commitResult(knowns, unknowns);
            // recap unknowns
            this._shuffleStudyPanel(unknowns);
        }
    },

    studyPanelNewContentAddedHandler: function(newContents, toPostToServer) {
        console.log('App::studyPanelNewContentAddedHandler(), newContents: ', newContents, 'toPostToServer: ', toPostToServer);
        if (toPostToServer) {
            // ajax post newContents
            this._commitResult([], newContents);
        }
        this._shuffleStudyPanel(newContents);
    },

    componentDidMount: function() {
        this._initStudyPanel(this.state.category);
    },

    _commitResult: function(knowns, unknowns) {
        console.log('App::_commitResult() knowns: ', knowns, ' unknowns: ', unknowns);
        StudyAPI.updateLeitnerRecord(knowns, unknowns, this.state.category);
    },

    _initStudyPanel: function(category) {
        console.log('App::_initStudyPanel() category: ', category);
        var component = this;
        var fontClass = category === "chinese_poem" ? "han_character_small" : "han_character";

        $.when(StudyAPI.getLeitnerRecord(category), StudyAPI.getProgress(category))
        .done(function(leitnerRecordResp, progressResp){
            console.log('App::_getHanzisAndStats() leitnerRecordResp: ', leitnerRecordResp, 'progressResp: ', progressResp);
            var hanzis = leitnerRecordResp[0].map(function(studyRecord) {
                    return studyRecord['hanzi']
                });
            component.setState({
                'hanzis': Util.shuffle(hanzis),
                'stats': progressResp[0],
                'recapMode': false,
                'fontClass': fontClass,
                'category': category
            });      
        });
    },

    _shuffleStudyPanel: function(hanzis) {
        console.log('App::_shuffleStudyPanel() hanzis: ', hanzis);
        this.setState({
            'hanzis': Util.shuffle(hanzis),
            'recapMode': true,
        });

        //this._refreshStats(this.state.category);
    },

    _refreshStats: function(category) {
        var component = this;
        console.log('App::_refreshStats() category:', category);
        $.when(StudyAPI.getProgress(category))
        .done(function(progressResp) {
            console.log('App::_getStats() progressResp: ', progressResp);
            component.setState({
                'stats': progressResp
            });
        });
    },

    render: function() {
        console.log('App::render() username:', username);
        return (
            <div>
                <HornbookNavBar categories={categories} username={username} navItemClickHandler={this.studyCategory} />
                <StudyPanel hanzis={this.state.hanzis} 
                    stats={this.state.stats} 
                    sessionDoneHandler={this.studyPanelSessionDoneHandler}
                    newContentAddedHandler={this.studyPanelNewContentAddedHandler}
                    recapMode={this.state.recapMode}
                    fontClass={this.state.fontClass} />
            </div>
        );
    }
});

ReactDOM.render(<App />, document.getElementById('app'));
