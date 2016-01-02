"use strict";

var React = require('react');
var ReactBootstrap = require('react-bootstrap');

var BadgeList = React.createClass({
    propTypes: {
        contents: React.PropTypes.array.isRequired,
    },

    render: function() {
        var contents = this.props.contents.map(function(content) {
            const ref = 'badgeList_' + content;
            return (<ReactBootstrap.Badge ref={ref} key={ref}>{content}</ReactBootstrap.Badge>)
        });
        return (
            <div>
                {contents}
            </div>
        )       
    }
});

module.exports = BadgeList;
