IMG_WIDTH = 320

angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})


.controller('ChannelCtrl', function($scope, $stateParams, Channels, Thumbnails, $cordovaSocialSharing, $ionicScrollDelegate) {
    //$scope.thumbnails = Thumbnails.get($stateParams.channelId)
    $scope.thumbnails = []
    Thumbnails.get($stateParams.channelId, $scope);
    $scope.channel = Channels.get($stateParams.channelId - 1)
    $scope.position = 0


    // share anywhere
	$scope.share = function (thumbnail) {
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}
	
	$scope.go_to_position = function (position) {
		$ionicScrollDelegate.$getByHandle("carousel").scrollTo(position/100*$scope.thumbnails.length*IMG_WIDTH, 0, true);

	}

	$scope.set_position = function () {
		pos = $ionicScrollDelegate.$getByHandle("carousel").getScrollPosition().left;
		$scope.position = pos / IMG_WIDTH;

	}
})
