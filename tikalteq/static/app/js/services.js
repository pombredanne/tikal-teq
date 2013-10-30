/**
 * Created by liorb on 10/13/13.
 */
'use strict';

TikalTeq.factory('CandidateService', function ($q, Restangular) {
    return {
         list: function () {
                Restangular.setBaseUrl("../../api/");
                //adjust to Django Rest API format
                Restangular.setResponseExtractor(
                    function(response, operation, what, url, deferred) {
                        if (operation === "getList") {
                            var newResponse = response.results;
                            newResponse._resultmeta = {
                                "count": response.count,
                                "next": response.next,
                                "previous": response.previous
                            };
                            return newResponse;
                        }
                        return response;
                    }
                )
                var deferred = $q.defer();
                var candidatesService = Restangular.all('candidates/').getList().then(function(data){
                   deferred.resolve(data);
                });
                return deferred.promise;
        }
    }
})

