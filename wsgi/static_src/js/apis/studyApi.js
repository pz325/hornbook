// $ = jQuery = require('jquery');
// require('../libs/notify');

var StudyAPI = (function() {
    var API_LEITNER_RECORD_URL = "/api/study/hanzi_study_record/leitner_record";
    var API_PROGRESS_URL = "/api/study/hanzi_study_record/progress";
    var API_CATEGORY_URL = "/api/study/category"
    
    var getCategories = function() {
        console.log('StudyAPI::getCategories()');
        return $.ajax({
            type: 'GET',
            url: API_CATEGORY_URL
        });
    };

    var getLeitnerRecord = function(category) {
        console.log('StudyAPI::getLeitnerRecord() category: ', category);
        return $.ajax({
            type: 'GET',
            url: API_LEITNER_RECORD_URL,
            data: {
                category_id: category['id'],
                num_retired: category['num_retired']
            }
        });
    };

    var getProgress = function(category) {
        console.log('StudyAPI::getProgress(): category: ', category);
        return $.ajax({
            type: 'GET',
            url: API_PROGRESS_URL,
            data: {
                category_id: category['id']
            }
        })
    }

    /*
     * @param knowns an array
     * @param unknowns an array
     * @param category string
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
                category_id: category['id'],
                grasped_hanzi: JSON.stringify(knowns), 
                new_hanzi: JSON.stringify(unknowns)
            },
            //data: data,
            dataType: "json",
            success: function(resp) {
                console.log('success with resp: ', resp);
                $.notify("Updated", "success");
            },
            error: function(resp) {
                console.log('failed with resp: ', resp);
                $.notify("Updating study history failed", "warn");
            }
            });
    };

    return {
        updateLeitnerRecord: updateLeitnerRecord,
        getLeitnerRecord: getLeitnerRecord,
        getProgress: getProgress,
        getCategories: getCategories
    };
})();

module.exports = StudyAPI;
