IMG_WIDTH = 320

angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})


.controller('ChannelCtrl', function($scope, $stateParams, Channels, Thumbnails, Video, $cordovaSocialSharing, $ionicScrollDelegate, $interval) {
    //$scope.thumbnails = Thumbnails.get($stateParams.channelId)
    $scope.thumbnails = []
    Thumbnails.get($stateParams.channelId, $scope);
    $scope.channel = Channels.get($stateParams.channelId)
    $scope.position = 0
    $scope.current_thumbnail = 0
    $scope.pressed = false;

    // share anywhere
	$scope.share_image = function () {
		thumbnail = $scope.thumbnails[$scope.current_thumbnail]
		console.log($scope.channel);
	    $cordovaSocialSharing.share('Look this image', $scope.channel.name, null, thumbnail.src);
	}

    // share anywhere
	$scope.share_video = function () {
		//call to api
	    Video.get($scope.thumbnails[$scope.first_thumbnail].id, int($scope.last_thumbnail - $scope.first_thumbnail + 1),
	    		function (data) {
			        $scope.video_url = data.clip_url;
				    $cordovaSocialSharing.share('Look this video', $scope.channel.name, null, $scope.video_url);
	    		}
	    	);

	}

	// cuando se mueve el slider	
	$scope.go_to_position = function (position) {
		// convert position to current_thumbnail
		$scope.current_thumbnail = position/100*$scope.thumbnails.length;

		// mueve el carousel
		$ionicScrollDelegate.$getByHandle("carousel").scrollTo($scope.current_thumbnail*IMG_WIDTH, 0, true);
	}

	$scope.go_to_thumbnail = function(thumbnail) {
		$scope.current_thumbnail =  thumbnail;
		// convert current_thumbnail to position
		$scope.position = $scope.current_thumbnail * 100 / $scope.thumbnails.length;

		// mover el slider
		if (!$scope.moving_carousel)
			$ionicScrollDelegate.$getByHandle("carousel").scrollTo($scope.current_thumbnail*IMG_WIDTH, 0, true);

	}

	// cuando se mueve el carousel
	$scope.set_position = function () {
		$scope.moving_carousel = true;
		pos = $ionicScrollDelegate.$getByHandle("carousel").getScrollPosition().left;
		$scope.go_to_thumbnail(pos / IMG_WIDTH)
		$scope.moving_carousel = false;
	}

	// funciones de grabacion
	$scope.handle_mousedown = function () {
		$scope.pressed = true;
		$scope.first_thumbnail = $scope.current_thumbnail;
		$scope.stop = $interval($scope.tick, 300);
	}

	$scope.handle_mouseup = function () {
		$scope.pressed = false;
		$scope.last_thumbnail = $scope.current_thumbnail;
		$interval.cancel($scope.stop);

		$scope.share_video();

	}

	$scope.tick = function () {
		if ($scope.pressed) {
			// advance
			$scope.go_to_thumbnail ($scope.current_thumbnail + 1)
		}
	}


})
