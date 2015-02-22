IMG_WIDTH = 320

angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})


.controller('ChannelCtrl', function($scope, $stateParams, Channels, Thumbnails, $cordovaSocialSharing, $ionicScrollDelegate) {
    //$scope.thumbnails = Thumbnails.get($stateParams.channelId)
    $scope.thumbnails = []
    Thumbnails.get($stateParams.channelId, $scope);
    $scope.channel = Channels.get($stateParams.channelId)
    $scope.position = 0
    $scope.current_thumbnail = 0

    // share anywhere
	$scope.share_image = function () {
		thumbnail = $scope.thumbnails[$scope.current_thumbnail]
		console.log($scope.channel);
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}

    // share anywhere
	$scope.share_video = function () {
		//call to api
		thumbnail = $scope.thumbnails[$scope.current_thumbnail]
	    $cordovaSocialSharing.share('Look this video', $scope.channel.name, null, thumbnail.src);
	}

	// cuando se mueve el slider	
	$scope.go_to_position = function (position) {
		// convert position to current_thumbnail
		$scope.current_thumbnail = position/100*$scope.thumbnails.length
		$ionicScrollDelegate.$getByHandle("carousel").scrollTo($scope.current_thumbnail*IMG_WIDTH, 0, true);

	}

	// cuando se mueve el carousel
	$scope.set_position = function () {
		pos = $ionicScrollDelegate.$getByHandle("carousel").getScrollPosition().left;
		$scope.current_thumbnail =  pos / IMG_WIDTH;
		// convert current_thumbnail to position
		$scope.position = $scope.current_thumbnail * 100 / $scope.thumbnails.length;
	}
})
