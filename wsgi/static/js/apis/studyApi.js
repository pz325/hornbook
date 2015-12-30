$ = jQuery = require('jquery');
var Notify = require('../libs/notify');

var StudyAPI = (function() {
    const API_LEITNER_RECORD_URL = "/api/study/hanzi_study_record/leitner_record";
    const API_PROGRESS_URL = "/api/study/hanzi_study_record/progress";
    
    var getLeitnerRecord = function(category) {
        console.log('StudyAPI::getLeitnerRecord() category: ', category);
        return $.ajax({
            type: 'GET',
            url: API_LEITNER_RECORD_URL,
            data: {
                category: category
            }
        });
    };

    var getProgress = function(category) {
        console.log('StudyAPI::getProgress(): category: ', category);
        return $.ajax({
            type: 'GET',
            url: API_PROGRESS_URL,
            data: {
                category: category
            }
        })
    }

    /*
     * @param knowns an array
     * @param unknowns an array
     * @return $.ajax()
     */
    var updateLeitnerRecord = function(knowns, unknowns, category) {
        console.log('StudyAPI::updateLeitnerRecord() knowns: ', knowns,
            ' unknowns: ', unknowns,
            'category: ', category);
        return $.ajax({
            type: "POST",
            url: API_LEITNER_RECORD_URL,
            data: {
                category: category,
                grasped_hanzi: JSON.stringify(knowns), 
                new_hanzi: JSON.stringify(unknowns)
            },
            //data: data,
            dataType: "json",
            success: function(resp) {
                console.log('success with resp: ', resp);
                Notify.notify("Updated", "success");
            },
            error: function(resp) {
                console.log('failed with resp: ', resp);
                Notify.notify("Updating study history failed", "warn");
            }
            });
    };

    var testMethod = function() {
        console.log(Notify);
    }

    return {
        updateLeitnerRecord: updateLeitnerRecord,
        getLeitnerRecord: getLeitnerRecord,
        getProgress: getProgress,
        testMethod: testMethod
    };
})();

module.exports = StudyAPI;
