var claqueteApp = angular.module('claqueteApp', ['ngRoute', 'myApp', 'myApp2','myApp3','vistoApp','queroVerApp','filtersApp']);

claqueteApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: 'main',  
            controller: 'mainCtrl'
        }).
        when('/full-recommendation', {
            templateUrl: 'full-recommendation',  
            controller: 'recoCtrl'
        }).
        when('/moviedetails/:tmdbID/:userID', {
            templateUrl: 'moviedetails',
            controller: 'movieCtrl'
        }).
        when('/watchedlistview', {
            templateUrl: 'watchedlist',
            controller: 'watchedListCtrl'
        }).
        when('/watchlistview', {
            templateUrl: 'watchlist',
            controller: 'watchlistCtrl'
        }).
        when('/filtersview/:genres/:language/:yearMin/:yearMax/:runtimeMin/:runtimeMax', {
            templateUrl: 'filters',
            controller: 'filtersCtrl'
        });
    }

]);

claqueteApp.config([
    '$httpProvider', function ($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrfToken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
]);