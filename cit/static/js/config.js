app.config(
	function ($routeProvider) {
		$routeProvider
			.when('/profile', {
				templateUrl: 'static/templates/profile.html'
			})
			
			.when('/', {
				templateUrl: 'static/templates/context.html'
			})
			.when('/report-issue/', {
				templateUrl: 'static/templates/report_issue.html',
				controller: 'UserNS'
			});			
	}
)
