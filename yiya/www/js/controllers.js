angular.module('starter.controllers', ['starter.services'])


.controller('ChannelsCtrl', function($scope) {
    $scope.channels = [
            {id: 1, name: 'Telefé'}, 
            {id: 2, name: 'Canal 13'}, 
            {id: 3, name: 'ESPN'},
      ];
})

