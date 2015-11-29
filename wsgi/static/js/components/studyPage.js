var csrftoken = Util.getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!Util.csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

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
                <ReactBootstrap.Label bsStyle='success'>grasped: {this.props.stats.grasped}</ReactBootstrap.Label>
            </div>
        );
    }
});


var ModelQuery = React.createClass({
    propTypes: {
        show: React.PropTypes.bool.isRequired,
        header: React.PropTypes.string.isRequired,
        contents: React.PropTypes.string.isRequired,
        no: React.PropTypes.func.isRequired,
        yes: React.PropTypes.func.isRequired
    },
    render: function() {
        return (
            <div>
                <ReactBootstrap.Modal show={this.props.show} onHide={this.props.no}>
                    <ReactBootstrap.Modal.Header closeButton>
                        <ReactBootstrap.Modal.Title>{this.props.header}</ReactBootstrap.Modal.Title>
                    </ReactBootstrap.Modal.Header>
                    <ReactBootstrap.Modal.Body>
                        {this.props.contents}
                    </ReactBootstrap.Modal.Body>
                    <ReactBootstrap.Modal.Footer>
                        <ReactBootstrap.ButtonToolbar>
                            <ReactBootstrap.Button bsStyle="info" onClick={this.props.yes}>Save</ReactBootstrap.Button>
                            <ReactBootstrap.Button onClick={this.props.no}>No</ReactBootstrap.Button>
                        </ReactBootstrap.ButtonToolbar>
                    </ReactBootstrap.Modal.Footer>
                </ReactBootstrap.Modal>
            </div>
        );
    }
});

/** 
 * A form to add new contents
 * Also display stats
 */
var NewContentForm = React.createClass({
    propTypes: {
        stats: React.PropTypes.shape({
            new: React.PropTypes.number,
            studying: React.PropTypes.number,
            grasped: React.PropTypes.number
        }).isRequired,
        newContents: React.PropTypes.array.isRequired,
        updateNewContents: React.PropTypes.func.isRequired,
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
        this.props.updateNewContents(event.target.value);
    },

    handleAddButtonClick: function() {
        if (this.props.newContents.length > 0) {
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
        const addButton = <ReactBootstrap.Button bsStyle="info" onClick={this.handleAddButtonClick}><ReactBootstrap.Glyphicon glyph="plus"/></ReactBootstrap.Button>;
        const stats = <StatLabels stats={this.props.stats} />;
        const newContentsStr = this.props.newContents ? this.props.newContents.join() : "";

        return (
            <div>
                <hr/>
                <div className="stat">
                    <ReactBootstrap.Input 
                        type="text"
                        value={this.state.rawNewContents}
                        placeholder="new content. space to separate" 
                        ref="newContents" 
                        onChange={this.handleNewContentsInputChange}
                        addonBefore={stats}    // add stat labels before NewContent input
                        buttonAfter={addButton}
                        help={"new contents: " + newContentsStr}/>                
                </div>
                <ModelQuery
                    show={this.props.showSaveQueryModel}
                    header="Save the following new contents to server"
                    contents={newContentsStr}
                    yes={this.saveNewContentToServer}
                    no={this.closeWithoutSavingToServer} />
            </div>
        );
    }
});

var Unknowns = React.createClass({
    propTypes: {
        unknowns: React.PropTypes.array.isRequired,
    },

    render: function() {
        var unknowns = this.props.unknowns.map(function(unknown) {
            return (<ReactBootstrap.Badge>{unknown}</ReactBootstrap.Badge>)
        });
        return (
            <div>
                {unknowns}
            </div>
        )
    }
});


var StudyComponent = React.createClass({
    propTypes: {
        hanzis: React.PropTypes.array.isRequired,
        hanziIndex: React.PropTypes.number.isRequired,
        addToKnowns: React.PropTypes.func.isRequired,
        hanziClass: React.PropTypes.string
    },
    render: function() {
        var hanzi = '';
        if (this.props.hanzis) {
            hanzi = this.props.hanzis[this.props.hanziIndex];
        }
        var hanziClass = this.props.hanziClass ? this.props.hanziClass : "han_character";

        return (
            <div>
                <span className={hanziClass} onClick={this.props.addToKnowns}>{hanzi}</span>
            </div>
        );
    }
});


var CATEGORY = $("#app").attr("category");

var StudyPage = React.createClass({
    getInitialState: function() {
        return {
            'hanzis': [],
            'hanziIndex': 0,
            'unknowns': [],
            'knowns': [],
            'stats': {},
            'recapMode': false,
            'newContents': [],
            'showSaveQueryModel': false
        };
    },
    
    addToKnowns: function() {
        this.updateProgress(true);
    },
    
    addToUnknowns: function() {
        this.updateProgress(false);
    },
    
    updateProgress: function(addToKnowns) {
        var oldState = this.state;
        if (addToKnowns) {
            oldState.knowns.push(this.state.hanzis[oldState.hanziIndex]);            
        } else {
            oldState.unknowns.push(this.state.hanzis[oldState.hanziIndex]);            
        }
        
        oldState.hanziIndex += 1;
        if (oldState.hanziIndex < this.state.hanzis.length) {
            this.setState(oldState);
        } else {
            if (!this.state.recapMode) {
                this.commitResult();
            }
            var hanzisToRecap = this.state.recapMode ? 
                Util.shuffle(this.state.hanzis):
                Util.shuffle(this.state.unknowns);
            oldState.hanziIndex = 0;
            oldState.unknowns = [];
            // recap
            this.recap(hanzisToRecap);
        }
    },

    commitResult: function() {
        var component = this;
        // commit to server
        var result = {
            "grasped_hanzi": this.state.knowns,
            "new_hanzi": this.state.unknowns
        };
        $.when(StudyAPI.updateLeitnerRecord(this.state.knowns, this.state.unknowns, CATEGORY))
        .done(function() {
            component.refreshStat();
        });
    },

    recap: function(newHanzis) {
        this.setState({
            'hanzis': Util.shuffle(newHanzis),
            'recapMode': true,
            'hanziIndex': 0,
            'knowns': [],
            'unknowns': [],
            'newContents': []
        });
        this.refreshStat();
    },

    refreshStat: function() {
        var component = this;
        $.when(StudyAPI.getProgress(CATEGORY))
        .done(function(progressResp) {
            component.setState({
                'stats': progressResp,
            });
        });
    },

    componentDidMount: function() {
        var component = this;
        $.when(StudyAPI.getLeitnerRecord(CATEGORY), StudyAPI.getProgress(CATEGORY))
        .done(function(leitnerRecordResp, progressResp){
            console.log(leitnerRecordResp);
            var hanzis = leitnerRecordResp[0].map(function(studyRecord) {
                    return studyRecord['hanzi']
                });
            component.setState({
                'hanzis': Util.shuffle(hanzis),
                'stats': progressResp[0]
            });
        });
    },
    
    getAddToRecapButton: function() {
        if (!this.state.recapMode) {
            return (<ReactBootstrap.Button bsStyle="info" onClick={this.addToUnknowns}>Add To Recap</ReactBootstrap.Button>);
        } else {
            return 'Recap mode';
        }
    },

    updateNewContents: function(rawNewContents) {
        this.setState({
            'newContents': rawNewContents.match(/\S+/g)
        })
    },

    showSaveQuery: function(show) {
        this.setState({
            'showSaveQueryModel': show
        })
    },

    addNewContents: function(save) {
        if (save) {
            StudyAPI.updateLeitnerRecord([], this.state.newContents, CATEGORY);
        }
        this.recap(this.state.newContents);
    },

    render: function() {
        const progressMax = this.state.hanzis.length;
        const progressNow = progressMax > 0 ? this.state.hanziIndex + 1 : 0;
        const hanziClass = CATEGORY === "chinese_poem" ? "han_character_small" : "han_character";

        return (
            <div>
                <NewContentForm 
                    stats={this.state.stats} 
                    newContents={this.state.newContents} 
                    updateNewContents={this.updateNewContents}
                    showSaveQuery={this.showSaveQuery} 
                    showSaveQueryModel={this.state.showSaveQueryModel}
                    addNewContents={this.addNewContents} />
                <ReactBootstrap.ProgressBar max={progressMax} now={progressNow} bsStyle="success" label="%(now)s of %(max)s" />
                <StudyComponent 
                    hanzis={this.state.hanzis} 
                    hanziIndex={this.state.hanziIndex} 
                    addToKnowns={this.addToKnowns}
                    hanziClass={hanziClass} />
                {this.getAddToRecapButton()}
                <Unknowns unknowns={this.state.unknowns} />
                <hr />
            </div>
        );
    }
});


ReactDOM.render(
    <StudyPage />,
    document.getElementById('app')
);