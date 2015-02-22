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
    	},
    	get: function ($channelId) {
    		return channels[$channelId - 1];
    	}
    }
})




.factory('Thumbnails', function () {
	var thumbnails = [
            [{hora: "10:00:00"}, {hora: "10:00:01"}, {hora: "10:00:02"}, {hora: "10:00:03"}], 
            [{hora: "10:00:10"}, {hora: "10:00:11"}, {hora: "10:00:12"}, {hora: "10:00:13"}], 
            [{hora: "10:00:20"}, {hora: "10:00:21"}, {hora: "10:00:22"}, {hora: "10:00:23"}], 
      ];

    return {
    	/*get: function (channelId) {
    		return thumbnails[channelId-1];
    	},*/
    	get: function() {
    		var res = [];
    		for (i=0;i<600;i++) {
    			res.push({
    				src: "img/messi.jpg",
    			});
    		}
    		return res;
    	}
    }
})

