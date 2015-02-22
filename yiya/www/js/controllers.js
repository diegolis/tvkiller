angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})


.controller('ChannelCtrl', function($scope, $stateParams, Channels, Thumbnails, $cordovaSocialSharing) {
    $scope.thumbnails = Thumbnails.get($stateParams.channelId)
    $scope.channel = Channels.get($stateParams.channelId - 1)

    // share anywhere
	$scope.share = function (thumbnail) {
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}
	

})

