var BASE_URL = "http://localhost:8000/";

function get_thumbnails($http, $log, channel_id) {
    var url = BASE_URL + "get_thumbs/" + channel_id;
    var retval = []

    $http.get(url)
    .success(function(data, status, headers, config) {
        retval = data
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
            {id: 1, name: 'Telefé'}, 
            {id: 2, name: 'Canal 13'}, 
            {id: 3, name: 'ESPN'},
      ];

    return {
    	all: function () {
    		return channels;
    	}
    }
})
.factory('thumbnails', function ($http, $log) {
    return function(channel_id) {
        get_thumbnails($http, $log, channel_id);;
    };
});
