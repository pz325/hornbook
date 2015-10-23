var Button = ReactBootstrap.Button;
var ProgressBar = ReactBootstrap.ProgressBar;

var stats = {'grasped': 50, 'new': 30, 'studying': 20};
var progress = {'max': 60, 'now': 28};
var hanzi = ['王', '张'];
var unknowns = ['东', '夏'];
var hanziIndex = 1;

var TestApp = React.createClass({  
  getInitialState: function() {
    return {};
  },
  componentDidMount: function() {
    var component = this;
    $.get("/api/study/hanzi_study_count/2", function(data) {
        console.log(data);
        component.setState(data);
    });
  },
  render: function() {
    var unknownBadges = unknowns.map(function(unknown){
        return (<ReactBootstrap.Badge>{unknown}</ReactBootstrap.Badge>)
    });
    return (
      <div>
        <hr/>
        <div>
            <ReactBootstrap.Label bsStyle='warning'>New: {stats.new}</ReactBootstrap.Label>
            <ReactBootstrap.Label bsStyle='info'>Studying: {stats.studying}</ReactBootstrap.Label>
            <ReactBootstrap.Label bsStyle='success'>grasped: {stats.grasped}</ReactBootstrap.Label>
        </div>
        <ProgressBar max={progress.max} now={progress.now} bsStyle="success" label="%(now)s of %(max)s" />
        <div className="han_character">
            {hanzi[hanziIndex]}
        </div>
        <ReactBootstrap.Button>Add To Recap</ReactBootstrap.Button>
        <div>
            {unknownBadges}
        </div>
        <hr/>
        {this.state.count}
      </div>
    );
  }
});

ReactDOM.render(
    // alertInstace,   
    React.createElement(TestApp, null),
    document.getElementById('content')
);