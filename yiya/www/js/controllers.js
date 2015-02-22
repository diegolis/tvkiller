angular.module('starter.controllers', ['starter.services'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})

