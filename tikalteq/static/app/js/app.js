/**
 * Created by liorb on 10/13/13.
 */
'use strict';

/* App Module */
var TikalTeq = angular.module('TikalTeq', ['ngRoute','restangular', 'ngGrid']).
  config(
        function(RestangularProvider) {
            RestangularProvider.setBaseUrl("../../api/");
            RestangularProvider.setResponseExtractor(
                function(response, operation, what, url) {
                    if (operation === "getList") {
                        // Use results as the return type, and save the result metadata
                        // in _resultmeta
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
        },
        ['$routeProvider',
        function($routeProvider) {
            $routeProvider.when('/candidates', {
                templateUrl: 'partials/candidate-list.html',
                controller: CandidateListCtrl,
                resolve: {
                    candidates: function (CandidateService) {
                        return CandidateService.list();
                    }
                }
            })
        }]
   );

