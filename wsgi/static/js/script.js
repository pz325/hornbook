// var $ = require('jquery');  
// var React = require('react');

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
    return (
      <div className="page">
        {this.state.count}
      </div>
    );
  }
});

React.render(  
  React.createElement(TestApp, null),
  document.getElementById('content')
);