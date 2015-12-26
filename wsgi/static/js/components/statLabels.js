"use strict";

var React = require('react');
var ReactBootstrap = require('react-bootstrap');

var StatLabels = React.createClass({
    propTypes: {
        stats: React.PropTypes.shape({
            new: React.PropTypes.number,
            studying: React.PropTypes.number,
            grasped: React.PropTypes.number
        }).isRequired
    },
    render: function() {
        return (
            <div>
                <ReactBootstrap.Label bsStyle='warning'>New: {this.props.stats.new}</ReactBootstrap.Label>
                <ReactBootstrap.Label bsStyle='info'>Studying: {this.props.stats.studying}</ReactBootstrap.Label>
                <ReactBootstrap.Label bsStyle='success'>Grasped: {this.props.stats.grasped}</ReactBootstrap.Label>
            </div>
        );
    }
});

module.exports = StatLabels;
