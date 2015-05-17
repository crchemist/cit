app.config(
	function ($routeProvider) {
		$routeProvider
			.when('/profile', {
				templateUrl: "static/templates/profile.html"
			})
			.when('/', {
				templateUrl: "static/templates/context.html"
			});
			
	}
)
