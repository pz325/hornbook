"use strict";

var React = require('react');
var ReactBootstrap = require('react-bootstrap');

var StatLabels = require('./statLabels');
var QueryModal = require('./queryModal');

/** 
 * A form to add new contents
 * Also display stats
 */
var NewContentForm = React.createClass({
    propTypes: {
        statLabels: React.PropTypes.element,
        addNewContents: React.PropTypes.func
    },

    getInitialState: function() {
        return {
            'rawNewContents': "",  // used for the controlled input
            'showModal': false
        };
    },

    handleNewContentsInputChange: function(event) {
        this.setState({
            'rawNewContents': event.target.value
        });
    },

    handleButtonAddClick: function() {
        if (this.state.rawNewContents.length > 0) {
            this.setState({
                'showModal': true
            });
        }
    },

    reset: function() {
        this.setState({
            'rawNewContents': "",
            'showModal': false
        });
    },

    closeWithoutSavingToServer: function() {
        this.props.addNewContents(this.getNewContentsArray(this.state.rawNewContents), false);
        this.reset();
    },

    saveNewContentToServer: function() {
        this.props.addNewContents(this.getNewContentsArray(this.state.rawNewContents), true);
        this.reset();
    },

    getNewContentsArray: function(rawNewContents) {
        var newContentsArray = [];
        if (rawNewContents) {
            newContentsArray = this.state.rawNewContents.match(/\S+/g);
        }
        return newContentsArray;
    },

    render: function() {
        const newContentsArray = this.getNewContentsArray(this.state.rawNewContents);
        const newContentsStr = newContentsArray.join();

        const buttonAdd = <ReactBootstrap.Button bsStyle="info" onClick={this.handleButtonAddClick} ref='NewContentForm_buttonAdd'><ReactBootstrap.Glyphicon glyph="plus"/></ReactBootstrap.Button>;
        

        return (
            <div>
                <hr/>
                <div>
                    <ReactBootstrap.Input 
                        type="text"
                        value={this.state.rawNewContents}
                        placeholder="new content. space to separate" 
                        ref="NewContentForm_inputNewContent" 
                        onChange={this.handleNewContentsInputChange}
                        addonBefore={this.props.statLabels}    // add stat labels before NewContent input
                        buttonAfter={buttonAdd}
                        help={"new contents: " + newContentsStr}/>                
                </div>
                <QueryModal
                    ref='NewContentForm_queryModal'
                    show={this.state.showModal}
                    title="Save the following new contents to server"
                    body={newContentsStr}
                    yes={this.saveNewContentToServer}
                    no={this.closeWithoutSavingToServer} />
            </div>
        );
    }
});

module.exports = NewContentForm;
