angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})


.controller('ChannelCtrl', function($scope, $stateParams, Channels, Thumbnails, $cordovaSocialSharing) {
    $scope.thumbnails = Thumbnails.get($stateParams.channelId)
    $scope.channel = Channels.get($stateParams.channelId - 1)
    $scope.position = 0

    // share anywhere
	$scope.share = function (thumbnail) {
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}
	
	$scope.go_to_thumbnail = function (thumbnail) {
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}

})

