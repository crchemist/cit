angular.module("CITApp").factory("Profile", ["$http",function ProfileFactory($http) {
	return {
		all: function() {
          return  $http.get('/auth/user-info/');
		},
		changesProfile: function(dataObj) {
			return $http.post('/auth/user/profile/', dataObj);
		}
		
	}
}]);
