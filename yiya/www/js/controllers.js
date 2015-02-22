angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})

.controller('ChannelCtrl', function($scope, $stateParams, thumbnails, $cordovaSocialSharing) {
    $scope.thumbnails = thumbnails($stateParams.channelId)

    // share anywhere
	$scope.share = function (thumbnail) {
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}
})
