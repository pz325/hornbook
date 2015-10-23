var stats = {'grasped': 50, 'new': 30, 'studying': 20};
var progress = {'max': 60, 'now': 28};
// var hanzis = ['王', '张'];
var unknowns = ['东', '夏'];
var hanziIndex = 1;

var StudyComponent = React.createClass({
    // main study component  
    getInitialState: function() {
        return {
            'progress': {
                'max': 0,
                'now': 0
            }, 
            'hanziIndex': 0,
            'unknowns': []
        };
    },
    componentDidMount: function() {
        var component = this;
        $.get("/api/study/hanzi_study_count/2", function(data) {
            console.log(data);
            component.setState(data);
        });
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
                <ReactBootstrap.ProgressBar max={this.state.progress.max} now={this.state.progress.now} bsStyle="success" label="%(now)s of %(max)s" />
                <div className="han_character">
                    {hanzi}
                </div>
                    <ReactBootstrap.Button bsStyle="info">Add To Recap</ReactBootstrap.Button>
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
        };
    },
    componentDidMount: function() {
        var component = this;
        $.get("/api/study/hanzi_study_record/leitner_record", function(data) {
            console.log(data);
            hanzis = data.map(function(studyRecord){
                    return studyRecord['hanzi']
                });
            console.log(data);
            component.setState({
                'hanzis': hanzis 
            });
        });
    },
    render: function() {
        console.log(this.state);
        return (
            <StudyComponent stats={stats} hanzis={this.state.hanzis}/>
        );
    }

});


ReactDOM.render(
    <HornbookComponent />,
    document.getElementById('content')
);