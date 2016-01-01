"use strict";

var React = require('react');

var ClickableSpan = React.createClass({
    propTypes: {
        content: React.PropTypes.string,
        clickHandler: React.PropTypes.func.isRequired,
        fontClass: React.PropTypes.string
    },

    render: function() {
        return (
            <div>
                <span className={this.props.fontClass} onClick={this.props.clickHandler}>{this.props.content}</span>
            </div>
        );
    }
});

module.exports = ClickableSpan;
