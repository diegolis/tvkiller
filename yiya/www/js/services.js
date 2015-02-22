var BASE_URL = "http://clips.infoad.tv:34455/";

function parse_thumbnails(thumbnails) {
	for (var i=0; i<thumbnails.length; i++) {
		thumbnails[i].src = BASE_URL + "get_thumb/" + thumbnails[i].id
	}
	return thumbnails;
}

function get_thumbnails($http, $log, $scope, channel_id) {
    var url = BASE_URL + "get_thumbs/" + channel_id;

    $http.get(url)
    .success(function(data, status, headers, config) {
    	data = parse_thumbnails(data);
    	$scope.thumbnails = data;
    })
    .error(function(data, status, headers, config) {
    	$scope.thumbnails = [];
    });
};

function get_video_url($http, $log, $scope, thumb_id, duration, func) {
    var url = BASE_URL + "make_clip/" + thumb_id + "/" + duration;
    $http.get(url)
    .success(function(data, status, headers, config) {
    	func(data);
    })
    .error(function(data, status, headers, config) {
    });
};

angular.module('starter.services', [])

.factory('Channels', function () {
	var channels = [
    		//FIXME: define as a dictionary
            {id: 1, name: 'Telefé'}, 
            {id: 2, name: 'Canal 13'}, 
            {id: 3, name: 'ESPN'},
      ];

    return {
    	all: function () {
    		return channels;
    	},
    	get: function (channelId) {
    		//FIXME
    		return channels[channelId-1];
    	}
    }
})

.factory('FakeThumbnails', function () {
    return {
    	get: function(channel_id, $scope) {
    		var res = [];
    		for (i=1;i<=639;i++) {
    			res.push({
    				id: i,
    				src: "img/thumbs/" + i + ".jpg",
    			});
    		}
    		$scope.thumbnails = res;
    	}
    }
})

.factory('Thumbnails', function ($http, $log) {
    return {
    	get: function(channel_id, $scope) {
        	return get_thumbnails($http, $log, $scope, channel_id);
    	}
    }
})

.factory('Video', function($http, $log) {
    return {
        get: function(thumb_id, duration, $scope) {
            /* Given the thumb id and the duration, 
             * returns the URL of the video. */
            return get_video_url($http, $log, $scope, thumb_id, duration);
        }
    };
});
