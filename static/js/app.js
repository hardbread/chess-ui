var app = angular.module('chessUiApp', [
        'ngResource',
        'ngAnimate',
        'ngRoute',
        'ngTouch',
        'ui.grid'
    ]) //********** Config app **********//
    .config(function ($routeProvider, $httpProvider, $logProvider) {

        //delete $httpProvider.defaults.headers.common['X-Requested-With'];

        $logProvider.debugEnabled(true);

        $routeProvider
            .when('/', {
                title: 'Tournaments',
                template: '<div id="grid1" ui-grid="gridOptions"></div>',
                controller: 'tournamentCtrl'
            })
            .when('/tournament/:tId', {
                title: 'Tournament - Matches',
                template: '<div id="grid1" ui-grid="gridOptions"></div>',
                controller: 'tournamentCtrl'
            })
            .when('/matches', {
                title: 'Tournament - Matches',
                template: '<div id="grid1" ui-grid="gridOptions"></div>',
                controller: 'matchCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    }) // ************ Init app ***********//
    .run(function ($rootScope) {
        var apiPort = 8000;
        var domain = 'localhost';
        $rootScope.apiConf = {
            apiServer: 'http://' + domain + ':' + apiPort + '/api'
        };

        $rootScope.menuList = [
            {
                title: 'Tournaments',
                link: '#/'
            },
            {
                title: 'Matches',
                link: '#/matches/'
            },
            {
                title: 'Players',
                link: '#/players/'
            }
        ];

        $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
            // Change Title page on route
            $rootScope.title = current.$$route.title;
        });

    });

// ************************//

app.factory('apiService', ['$rootScope', '$http', '$log', '$q', function ($rootScope, $http, $log, $q) {
    var method = {};

        method.get = function(url){
                        var deferred = $q.defer();
                        var path = $rootScope.apiConf.apiServer + url;

                        $http.get(path, {cache: true})
                        .then(function(data){
                            $log.debug("API service request successfully: ", data.data);
                            deferred.resolve(data);
                        }, function(data){
                            $log.debug("API service request error: ", data.data);
                            deferred.reject(data);
                        });
                        return deferred.promise;
                     };
    return method;
}]);

app.controller('tournamentCtrl', ['$scope', '$log', 'apiService', function ($scope, $log, apiService) {

    $scope.tournamentModel = [];

    $scope.gridOptions = {
      data: 'tournamentModel',
      columnDefs: [
        { name: 'title',
            cellTemplate:
                '<a class="ui-grid-menu" link-to="tournament/{{row.entity.id}}/">' +
                '{{ row.entity.title }}</a>'
        },
        { name: 'description' },
        { name: 'startDate'},
        { name: 'endDate'},
        { name: 'winner',
            cellTemplate:
                '<a class="ui-grid-menu" link-to="player/{{row.entity.winner.id}}/">' +
                '{{ row.entity.winner.firstName }} {{ row.entity.winner.lastName }}</a>',
            displayName: 'Winner'}
     ]
    };
    // get model
    apiService.get('/tournaments/').then(function(data){
        if (data.status == 200){
            $scope.tournamentModel = data.data.responses;
            $log.debug('tournamentCtrl: $scope.tournamentModel=',  $scope.tournamentModel);
        }
    });

}]);


app.directive('mainMenu', ['$rootScope', function ($rootScope) {
        return {
            restrict: 'E',
            template: '<div class="block-text" id="main-menu">' +
                            '<ul ng-repeat=" el in menuList">' +
                                '<li class="block-text"><a href="{{ el.link }}">{{ el.title }}</a></li>' +
                            '</ul>' +
                      '</div>'
        }
}]);

app.directive('linkTo', ['$location', function ($location) {
        return {
            restrict: 'A',
            scope: {},
            link: function(scope, element, attrs) {
                attrs.$set('href', '#'+ ($location.path() != '/' ? $location.path(): '') + '/' + attrs.linkTo);
            }
        }
}]);


