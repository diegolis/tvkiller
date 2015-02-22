angular.module('starter.services', ['ngResource'])


.factory('Channels', function ($resource) {
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
});

