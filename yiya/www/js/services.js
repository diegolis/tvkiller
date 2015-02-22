angular.module('starter.services', ['ngResource'])


.factory('Channels', function ($resource) {
    return ['Telefé', 'Canal 13', 'ESPN'];
});
