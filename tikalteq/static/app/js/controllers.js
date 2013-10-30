/**
 * Created by liorb on 10/13/13.
 */
'use strict';

/* Controllers */

function CandidateListCtrl($scope, candidates) {
    $scope.candidates = candidates,
    $scope.gridData = {
       data: 'candidates',
       columnDefs: [{field: 'first_name', displayName: 'Name'}, {field:'last_name', displayName:'Last Name'}]
    }
}
