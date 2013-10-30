/**
 * Created by liorb on 10/13/13.
 */
'use strict';

TikalTeq.factory('CandidateService', function ($q, Restangular) {
    return {
         list: function () {
            var deferred = $q.defer();
            var candidatesService = Restangular.all('candidates/').getList().then(function(data){
               deferred.resolve(data);
            });
            return deferred.promise;
        }
    }
})

