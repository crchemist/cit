app.config(function ($translateProvider) {

    var language = (window.navigator.languages)[0];
    var userLanguage;

        if (language.length >2) {
            userLanguage = language.slice(0,2)
        } else {userLanguage = language}

  $translateProvider.translations('uk', {
    SIGN_IN_WITH_FACEBOOK: 'Увійти через Facebook',
    LOGOUT: 'Вийти',
    HOME: 'Головна',
    LOGO: 'Логотип',
    WARNING: 'Увага',
    PROFILE: 'Профіль',
    REPRT_ISSUE: 'Повідомити про забруднення',
    SUBJECT: 'Тема',
    COMMENT: 'Коментар',
    SUBMIT: 'Повідомити'
  });
   $translateProvider.translations('en', {
    SIGN_IN_WITH_FACEBOOK: 'Sign in with Facebook',
    LOGOUT: 'Logout',
    HOME: 'Home',
    LOGO: 'Logo',
    WARNING: 'Warning',
    PROFILE: 'Profile',
    REPRT_ISSUE: 'Report about issue',
    SUBJECT: 'Subject',
    COMMENT: 'Comment'    
  });
  
  $translateProvider.preferredLanguage(userLanguage);
 });

//Use filter 'traslate' for translation inside of attributes and buttons
//For instance, {{'SUBMIT' | translate}}
app.filter('translate', ['$rootScope', function($rootScope) {
  var language = (window.navigator.languages)[0];
  var userLanguage;
        if (language.length >2) {
            userLanguage = language.slice(0,2)
        } else {userLanguage = language}
  
 var translations = {
    'uk': { 'SUBMIT': 'Повідомити',
            'WRITE_SUBJECT': 'Задайте тему тут...',
            'WRITE_COMMENT': 'Залиште коментар тут...'

           },
    'en': { 'SUBMIT': 'Submit',
            'WRITE_SUBJECT': 'Type subject here...',
            'WRITE_COMMENT': 'Type comment here...'
          }
    };
  $rootScope.currentLanguage = userLanguage;
      return function(label) {
      return translations[$rootScope.currentLanguage][label];
  };
}]);