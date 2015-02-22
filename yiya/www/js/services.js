var BASE_URL = "http://192.168.0.116:8000/";

function parse_thumbnails(thumbnails) {
	for (var thumbnail in thumbnails) {
		thumbnail.src = BASE_URL + "get_thumb/" + thumbnail.id
	}

}

function get_thumbnails($http, $log, channel_id) {
    var url = BASE_URL + "get_thumbs/" + channel_id;
    var retval = [];

    $http.get(url)
    .success(function(data, status, headers, config) {
    	parse_thumbnails(data);
    	console.log(data);
        retval = data;
    })
    .error(function(data, status, headers, config) {
        retval = []
    });
    $log.info("Returning:" + retval);
    return retval;
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


/*

.factory('Thumbnails', function () {
    return {
    	get: function() {
    		var res = [];
    		for (i=1;i<=639;i++) {
    			res.push({
    				src: "img/thumbs/" + i + ".jpg",
    			});
    		}
    		return res;
    	}
    }
})
*/


.factory('Thumbnails', function ($http, $log) {
    return {
    	get: function(channel_id) {
        	return get_thumbnails($http, $log, channel_id);
    	}
    }
})
