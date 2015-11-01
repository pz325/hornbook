// var stats = {'grasped': 50, 'new': 30, 'studying': 20};
var unknowns = ['东', '夏'];
var hanziIndex = 1;

var API_LEITNER_RECORD_URL = "/api/study/hanzi_study_record/leitner_record";
var API_PROGRESS_URL = "/api/study/hanzi_study_record/progress";

var StudyComponent = React.createClass({
    // main study component  
    getInitialState: function() {
        return {
            'hanziIndex': 0,
            'unknowns': [],
            'knowns': []
        };
    },
    componentDidMount: function() {
        var oldState = this.state;
        this.setState(oldState);
    },
    addToKnowns: function() {
        var oldState = this.state;
        oldState.knowns.push(this.props.hanzis[oldState.hanziIndex]);
        oldState.hanziIndex += 1;
        this.setState(oldState);
    },
    addToUnknowns: function() {
        var oldState = this.state;
        oldState.unknowns.push(this.props.hanzis[oldState.hanziIndex]);
        oldState.hanziIndex += 1;
        this.setState(oldState);
    },
    render: function() {
        var unknownBadges = this.state.unknowns.map(function(unknown){
            return (<ReactBootstrap.Badge>{unknown}</ReactBootstrap.Badge>)
        });
        var hanzi = '';
        if (this.props.hanzis) {
            hanzi = this.props.hanzis[this.state.hanziIndex];
        } 
        return (
            <div>
                <hr/>
                <div>
                    <ReactBootstrap.Label bsStyle='warning'>New: {this.props.stats.new}</ReactBootstrap.Label>
                    <ReactBootstrap.Label bsStyle='info'>Studying: {this.props.stats.studying}</ReactBootstrap.Label>
                    <ReactBootstrap.Label bsStyle='success'>grasped: {this.props.stats.grasped}</ReactBootstrap.Label>
                </div>
                <ReactBootstrap.ProgressBar max={this.props.hanzis.length} now={this.state.hanziIndex+1} bsStyle="success" label="%(now)s of %(max)s" />
                <div className="han_character" onClick={this.addToKnowns}>
                    {hanzi}
                </div>
                    <ReactBootstrap.Button bsStyle="info" onClick={this.addToUnknowns}>Add To Recap</ReactBootstrap.Button>
                <div>
                    {unknownBadges}
                </div>
                <hr/>
                {this.state.count}
            </div>
        );
    }
});



var HornbookComponent = React.createClass({
    getInitialState: function() {
        return {
            'hanzis': [],
            'stats': {}
        };
    },
    componentDidMount: function() {
        var component = this;
        $.when($.get(API_LEITNER_RECORD_URL), $.get(API_PROGRESS_URL))
        .done(function(leitnerRecordResp, progressResp){
            var hanzis = leitnerRecordResp[0].map(function(studyRecord) {
                    return studyRecord['hanzi']
                });
            component.setState({
                'hanzis': hanzis,
                'stats': progressResp[0]
            });
        });
    },
    render: function() {
        return (
            <StudyComponent hanzis={this.state.hanzis} stats={this.state.stats}/>
        );
    }
});


ReactDOM.render(
    <HornbookComponent />,
    document.getElementById('content')
);