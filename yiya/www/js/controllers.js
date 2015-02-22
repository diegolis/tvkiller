angular.module('starter.controllers', ['starter.services', 'ngCordova'])


.controller('ChannelsCtrl', function($scope, Channels) {
    $scope.channels = Channels.all()
})

.controller('ChannelCtrl', function($scope, $stateParams, thumbnails, $cordovaSocialSharing) {
    $scope.thumbnails = thumbnails($stateParams.channelId)

    // share anywhere
	$scope.share = function () {
	    $cordovaSocialSharing.share('This is my message', 'Subject string', null, 'http://www.mylink.com');
	}
})
