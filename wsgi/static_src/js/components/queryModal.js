"use strict";

var React = require('react');
var ReactBootstrap = require('react-bootstrap');

var QueryModal = React.createClass({
    propTypes: {
        show: React.PropTypes.bool.isRequired,
        title: React.PropTypes.string.isRequired,
        body: React.PropTypes.string.isRequired,
        no: React.PropTypes.func.isRequired,
        yes: React.PropTypes.func.isRequired
    },
    render: function() {
        return (
            <div>
                <ReactBootstrap.Modal ref="modalDialog" show={this.props.show} onHide={this.props.no}>
                    <ReactBootstrap.Modal.Header closeButton>
                        <ReactBootstrap.Modal.Title ref="title">{this.props.title}</ReactBootstrap.Modal.Title>
                    </ReactBootstrap.Modal.Header>
                    <ReactBootstrap.Modal.Body ref="body">
                        {this.props.body}
                    </ReactBootstrap.Modal.Body>
                    <ReactBootstrap.Modal.Footer>
                        <ReactBootstrap.ButtonToolbar>
                            <ReactBootstrap.Button bsStyle="info" onClick={this.props.yes} ref="buttonSave">Save</ReactBootstrap.Button>
                            <ReactBootstrap.Button onClick={this.props.no} ref="buttonNo">No</ReactBootstrap.Button>
                        </ReactBootstrap.ButtonToolbar>
                    </ReactBootstrap.Modal.Footer>
                </ReactBootstrap.Modal>
            </div>
        );
    }
});

module.exports = QueryModal;
