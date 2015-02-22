angular.module('starter.controllers', ['starter.services'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})


.controller('ChannelCtrl', function($scope, $stateParams, Thumbnails) {
    $scope.thumbnails = Thumbnails.get($stateParams.channelId)
})

