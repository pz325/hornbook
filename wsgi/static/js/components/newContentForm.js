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
        statLabels: React.PropTypes.instanceOf(StatLabels).isRequired,
        showSaveQuery: React.PropTypes.func.isRequired,
        showSaveQueryModel: React.PropTypes.bool.isRequired,
        addNewContents: React.PropTypes.func.isRequired
    },

    getInitialState: function() {
        return {
            'rawNewContents': "",  // used for the controlled input
        };
    },

    handleNewContentsInputChange: function(event) {
        this.setState({
            'rawNewContents': event.target.value
        });
    },

    handleAddButtonClick: function() {
        if (this.state.rawNewContents.length > 0) {
            this.props.showSaveQuery(true);
        }
    },

    reset: function() {
        this.setState({
            'rawNewContents': "",
        });
    },

    closeWithoutSavingToServer: function() {
        this.props.showSaveQuery(false);
        this.props.addNewContents(false);
        this.reset();
    },
    saveNewContentToServer: function(){
        this.props.showSaveQuery(false);
        this.props.addNewContents(true);
        this.reset();
    },

    render: function() {
        var newContentArray = [];
        var newContentsStr = "";
        if (this.state.rawNewContents)
        {
            newContentArray = this.state.rawNewContents.match(/\S+/g);
            newContentsStr = newContentArray.join();
        }

        const addButton = <ReactBootstrap.Button bsStyle="info" onClick={this.handleAddButtonClick}><ReactBootstrap.Glyphicon glyph="plus"/></ReactBootstrap.Button>;
        

        return (
            <div>
                <hr/>
                <div>
                    <ReactBootstrap.Input 
                        type="text"
                        value={this.state.rawNewContents}
                        placeholder="new content. space to separate" 
                        ref="newContents" 
                        onChange={this.handleNewContentsInputChange}
                        addonBefore={this.props.statLabels}    // add stat labels before NewContent input
                        buttonAfter={addButton}
                        help={"new contents: " + newContentsStr}/>                
                </div>
                <QueryModal
                    show={this.props.showSaveQueryModel}
                    title="Save the following new contents to server"
                    body={newContentsStr}
                    yes={this.saveNewContentToServer}
                    no={this.closeWithoutSavingToServer} />
            </div>
        );
    }
});

module.exports = NewContentForm;
