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
    NAME: "Ім'я",
    SURNAME: 'Прізвище',
    ORGANIZATION: 'Організація',
    PROFILE: 'Профіль',
    REPRT_ISSUE: 'Повідомити про забруднення',
    SUBJECT: 'Тема',
    DESCRIPTION: 'опис',
    SUBMIT: 'Повідомити',
  });
   $translateProvider.translations('en', {
    SIGN_IN_WITH_FACEBOOK: 'Sign in with Facebook',
    LOGOUT: 'Logout',
    HOME: 'Home',
    LOGO: 'Logo',
    WARNING: 'Warning',
    NAME: 'Name',
    SURNAME: 'Surname',
    ORGANIZATION: 'Organization',
    PROFILE: 'Profile',
    REPRT_ISSUE: 'Report about issue',
    SUBJECT: 'Subject',
    DESCRIPTION: 'Description'   
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
    'uk': { 'SUBMIT': 'Підтвердити',
            'WRITE_SUBJECT': 'Задайте тему тут...',
            'WRITE_COMMENT': 'Залиште коментар тут...',
            'SELECT': 'Вибрати організацію...',
            'FILTER': 'Фільтрувати за..'

           },
    'en': { 'SUBMIT': 'Submit',
            'WRITE_SUBJECT': 'Type subject here...',
            'WRITE_COMMENT': 'Type comment here...',
            'SELECT': 'Select organization...',
            'FILTER': 'Filter'
          }
    };
  $rootScope.currentLanguage = userLanguage;
      return function(label) {
      return translations[$rootScope.currentLanguage][label];
  };
}]);